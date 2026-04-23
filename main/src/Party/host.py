import socket
import threading
import time
import os
import json
# Assuming your folder structure allows these relative imports
from .poker import start_deal, update_board, winer, detect_hand

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

def waiting():
    players = {}
    ip = get_ip()
    print(f"Your IP is: {ip}")
    message = "What's your name?"
    print("How many players are going to play?")
    max_number_players = int(input())
    number_players = 0
    
    while number_players < max_number_players:
        print(f"Waiting for player {number_players + 1}...")
        conexion, address = server.accept()
        conexion.send(message.encode('utf-8'))
        received_message = conexion.recv(1024).decode('utf-8')
        
        players[conexion] = {
            "name": received_message, 
            "money": 5000, 
            "conexion": conexion, 
            "deck": [],
            "folded": False 
        }
        number_players += 1
        print(f"{received_message} connected")
        
    print("All players connected, starting the game...")
    return players, max_number_players

def betting_round(players, middle_deck, round_level):
    # Determine community cards based on the round
    # round_level 0=Flop(3), 1=Turn(4), 2=River(5)
    cards_to_show_map = [3, 4, 5]
    cards_on_table = middle_deck[:cards_to_show_map[round_level]]

    # High-level logic: Every player gets a turn
    for conexion in players:
        if players[conexion].get("folded", False): 
            continue

        # 1. Identify the player's current best hand to help them out
        hand_type, _ = detect_hand(players[conexion]["deck"], cards_on_table)

        # 2. Send current status
        data = {
            "type": "ACTION_REQUIRED",
            "hand": players[conexion]["deck"],
            "board": cards_on_table,
            "current_hand_type": hand_type, 
            "money": players[conexion]["money"],
            "message": f"Your turn, {players[conexion]['name']}! What's your move?"
        }
        conexion.send((json.dumps(data) + "\n").encode('utf-8'))

        # 3. Wait for action
        try:
            response_raw = conexion.recv(1024).decode('utf-8').strip()
            if response_raw:
                resp = json.loads(response_raw.split("\n")[0])
                action = resp.get("action", "").lower()

                if action == "raise":
                    # ASK FOR AMOUNT
                    ask_amount = {"type": "ASK_AMOUNT", "message": "How much do you want to raise?"}
                    conexion.send((json.dumps(ask_amount) + "\n").encode('utf-8'))
                    
                    # Receive the specific number
                    amount_raw = conexion.recv(1024).decode('utf-8').strip()
                    amount_data = json.loads(amount_raw.split("\n")[0])
                    raise_value = int(amount_data.get("amount", 0))
                    
                    # Subtract money
                    players[conexion]["money"] -= raise_value
                    print(f"DEBUG: {players[conexion]['name']} raised ${raise_value}")
                    
                elif action == "fold":
                    players[conexion]["folded"] = True
                    print(f"DEBUG: {players[conexion]['name']} folded.")
                else:
                    print(f"DEBUG: {players[conexion]['name']} chose {action}.")
        except Exception as e:
            print(f"Error during betting: {e}")

def start_game():
    # 1. Setup
    players, max_num = waiting()
    
    # 2. Deal
    players, middle_deck = start_deal(players) 
    
    # --- ROUND 1: FLOP (3 cards) ---
    print("\n--- ROUND 1: FLOP ---")
    update_board(players, middle_deck, 0)
    betting_round(players, middle_deck, 0)

    # --- ROUND 2: TURN (4 cards) ---
    print("\n--- ROUND 2: TURN ---")
    update_board(players, middle_deck, 1)
    betting_round(players, middle_deck, 1)

    # --- ROUND 3: RIVER (5 cards) ---
    print("\n--- ROUND 3: RIVER ---")
    update_board(players, middle_deck, 2)
    betting_round(players, middle_deck, 2)
    
    # --- END GAME: WINNER ---
    print("\nEvaluating final hands...")
    results = []
    for conn in players:
        if not players[conn].get("folded", False):
            rank_name, rank_val = detect_hand(players[conn]["deck"], middle_deck)
            results.append((rank_name, rank_val, players[conn]["name"]))
    
    if results:
        winner = winer(results) # From poker.py
        # Send GAME_OVER to everyone with the CORRECT KEYS
        for conn in players:
            msg = {
                "type": "GAME_OVER",
                "winner_name": winner[2],
                "winner_hand": winner[0].replace("_", " ")
            }
            conn.send((json.dumps(msg) + "\n").encode('utf-8'))
    else:
        print("Everyone folded. No winner.")

# Start
if __name__ == "__main__":
    start_game()