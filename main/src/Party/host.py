import socket
import threading
import time
import os
import json
from poker import start_deal, update_board, winer, detect_hand

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5555))
server.listen()

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        mi_ip = s.getsockname()[0] 
        s.close()
        return mi_ip
    except Exception:
        return "127.0.0.1"

def broadcast_status(players, board, pot):
    """Update all players' screens simultaneously."""
    for conn in players:
        # We check the strength for each specific player
        hand_type, _ = detect_hand(players[conn]["deck"], board)
        data = {
            "type": "WAIT_TURN", 
            "hand": players[conn]["deck"],
            "board": board,
            "current_hand_type": hand_type,
            "money": players[conn]["money"],
            "pot": pot
        }
        try:
            conn.send((json.dumps(data) + "\n").encode('utf-8'))
        except:
            pass

def waiting():
    players = {}
    ip = get_ip()
    print(f"Server started at: {ip}:5555")
    print("If you want to connect use 127.0.0.1")
    print("How many players for this session?")
    try:
        max_number_players = int(input(">> "))
    except ValueError:
        max_number_players = 2 # Default
        
    number_players = 0
    while number_players < max_number_players:
        print(f"Waiting for player {number_players + 1}...")
        conexion, address = server.accept()
        conexion.send("What's your name?".encode('utf-8'))
        received_message = conexion.recv(1024).decode('utf-8')
        
        players[conexion] = {
            "name": received_message, 
            "money": 5000, 
            "conexion": conexion, 
            "deck": [],
            "folded": False 
        }
        number_players += 1
        print(f"Player '{received_message}' joined the table.")
        
    return players, max_number_players

def betting_round(players, middle_deck, round_level, pot):
    cards_map = [3, 4, 5]
    board = middle_deck[:cards_map[round_level]]
    highest_bet = 0  
    player_spent = {conn: 0 for conn in players} 
    
    # 1. ROUND ANTE ($100 fee)
    for conn in players:
        if not players[conn]["folded"]:
            players[conn]["money"] -= 100
            pot += 100

    broadcast_status(players, board, pot)

    # 2. BETTING LOOP
    round_finished = False
    while not round_finished:
        round_finished = True 

        for conn in players:
            if players[conn]["folded"]: continue
            
            to_call = highest_bet - player_spent[conn]
            # Skip if they already matched the high bet
            if to_call == 0 and highest_bet > 0:
                continue

            # Update everyone's UI before this player's turn
            broadcast_status(players, board, pot)

            hand_type, _ = detect_hand(players[conn]["deck"], board)
            data = {
                "type": "ACTION_REQUIRED",
                "hand": players[conn]["deck"],
                "board": board,
                "current_hand_type": hand_type,
                "money": players[conn]["money"],
                "pot": pot,
                "to_call": to_call,
                "message": f"To Call: ${to_call} | Round Highest: ${highest_bet}"
            }
            conn.send((json.dumps(data) + "\n").encode('utf-8'))

            try:
                raw_resp = conn.recv(1024).decode('utf-8').strip().split("\n")[0]
                resp = json.loads(raw_resp)
                action = resp.get("action", "").lower()

                if action == "fold":
                    players[conn]["folded"] = True
                
                elif action in ["check", "call"]:
                    cost = to_call
                    players[conn]["money"] -= cost
                    player_spent[conn] += cost
                    pot += cost

                elif action == "raise":
                    conn.send((json.dumps({"type": "ASK_AMOUNT", "message": "Extra amount?"}) + "\n").encode('utf-8'))
                    amt_raw = conn.recv(1024).decode('utf-8').strip().split("\n")[0]
                    amt_data = json.loads(amt_raw)
                    
                    # Safety check for non-numeric input
                    try:
                        subida = int(amt_data.get("amount", 0))
                    except ValueError:
                        subida = 0

                    total_a_pagar = to_call + subida
                    players[conn]["money"] -= total_a_pagar
                    player_spent[conn] += total_a_pagar
                    pot += total_a_pagar
                    
                    highest_bet = player_spent[conn] 
                    round_finished = False # Someone raised, everyone must act again
            except:
                pass

    return pot

def start_game():
    players, max_num = waiting()
    players, middle_deck = start_deal(players) 
    total_pot = 0

    # Main Rounds: Flop, Turn, River
    for i in range(3):
        total_pot = betting_round(players, middle_deck, i, total_pot)

    # FINAL SHOWDOWN
    print("\nGame Over. Calculating winners...")
    results = []
    for conn in players:
        if not players[conn].get("folded", False):
            rank_name, rank_val = detect_hand(players[conn]["deck"], middle_deck)
            results.append((rank_name, rank_val, players[conn]["name"]))
    
    if results:
        winner = winer(results) 
        for conn in players:
            msg = {
                "type": "GAME_OVER",
                "winner_name": winner[2],
                "winner_hand": winner[0].replace("_", " ")
            }
            conn.send((json.dumps(msg) + "\n").encode('utf-8'))
    else:
        print("No players left. Pot goes to the house!")

if __name__ == "__main__":
    start_game()