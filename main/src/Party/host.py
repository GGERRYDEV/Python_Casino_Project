import socket
import json
import os
import time
from poker import start_deal, update_board, winer, detect_hand

# --- CONFIGURACIÓN DE RED ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5555))
server.listen()

DB_FILE = "bank.json"

# --- PERSISTENCIA Y UTILIDADES ---
def save_data(players_data):
    with open(DB_FILE, "w") as f:
        json.dump(players_data, f, indent=4)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        mi_ip = s.getsockname()[0] 
        s.close()
        return mi_ip
    except:
        return "127.0.0.1"

def broadcast_status(players, board, pot):
    """Refresca la pantalla de todos los jugadores."""
    for conn in list(players.keys()):
        hand_type, _ = detect_hand(players[conn]["deck"], board)
        data = {
            "type": "WAIT_TURN", 
            "hand": players[conn]["deck"],
            "board": board,
            "current_hand_type": hand_type,
            "money": players[conn]["money"],
            "pot": pot
        }
        try: conn.send((json.dumps(data) + "\n").encode('utf-8'))
        except: pass

# --- LÓGICA DE APUESTAS ---
def betting_round(players, middle_deck, round_level, pot):
    cards_map = [3, 4, 5]
    board = middle_deck[:cards_map[round_level]]
    highest_bet = 0  
    player_spent = {conn: 0 for conn in players} 
    
    # ANTE ($100)
    for conn in players:
        if not players[conn]["folded"]:
            cost = min(players[conn]["money"], 100)
            players[conn]["money"] -= cost
            pot += cost

    round_finished = False
    while not round_finished:
        round_finished = True 
        for conn in list(players.keys()):
            if players[conn]["folded"] or players[conn]["money"] <= 0: continue
            
            to_call = highest_bet - player_spent[conn]
            if to_call == 0 and highest_bet > 0: continue

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
                "message": f"To match: ${highest_bet}"
            }
            conn.send((json.dumps(data) + "\n").encode('utf-8'))

            try:
                raw_resp = conn.recv(1024).decode('utf-8').strip().split("\n")[0]
                resp = json.loads(raw_resp)
                action = resp.get("action", "").lower()

                if action == "fold":
                    players[conn]["folded"] = True
                    print(f"[LOG] {players[conn]['name']} folded.")
                elif action in ["check", "call"]:
                    cost = min(players[conn]["money"], to_call)
                    players[conn]["money"] -= cost
                    player_spent[conn] += cost
                    pot += cost
                    print(f"[LOG] {players[conn]['name']} matched the bet.")
                elif action == "raise":
                    max_raise = players[conn]["money"] - to_call
                    conn.send((json.dumps({"type": "ASK_AMOUNT", "message": f"Max raise: ${max_raise}"}) + "\n").encode('utf-8'))
                    amt_raw = conn.recv(1024).decode('utf-8').strip().split("\n")[0]
                    subida = int(json.loads(amt_raw).get("amount", 0))
                    
                    if subida > max_raise: subida = max_raise
                    
                    total_pago = to_call + subida
                    players[conn]["money"] -= total_pago
                    player_spent[conn] += total_pago
                    pot += total_pago
                    highest_bet = player_spent[conn]
                    round_finished = False 
                    print(f"[LOG] {players[conn]['name']} raised to ${highest_bet}.")
            except: pass
    return pot

# --- JUEGO ---
def play_one_hand(players):
    for conn in players:
        players[conn]["folded"] = False
        players[conn]["deck"] = []

    players_list, middle_deck = start_deal(players) 
    total_pot = 0

    for i in range(3):
        active = [c for c in players if not players[c]["folded"]]
        if len(active) <= 1: break
        total_pot = betting_round(players, middle_deck, i, total_pot)

    active = [c for c in players if not players[c]["folded"]]
    if len(active) == 1:
        winner_conn = active[0]
        winner_name, winner_hand = players[winner_conn]["name"], "Last player standing"
    else:
        results = []
        for c in active:
            h_type, h_val = detect_hand(players[c]["deck"], middle_deck)
            results.append((h_type, h_val, players[c]["name"]))
        best = winer(results)
        winner_name, winner_hand = best[2], best[0]
        winner_conn = next(c for c in players if players[c]["name"] == winner_name)

    players[winner_conn]["money"] += total_pot
    print(f"[GAME] Hand finished. Winner: {winner_name} (+${total_pot})")

    for conn in list(players.keys()):
        msg = {"type": "GAME_OVER", "winner_name": winner_name, "winner_hand": winner_hand, "money": players[conn]["money"]}
        try: conn.send((json.dumps(msg) + "\n").encode('utf-8'))
        except: pass

# --- MAIN ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*40)
    print("      POKER SERVER CORE V3.0")
    print(f"      IP: {get_ip()} | PORT: 5555")
    print("If you are the host in your own machine use: 127.0.0.1")
    print("="*40)
    
    saved_balances = load_data()
    players = {}
    print("\n[?] How many players will join?")
    try:
        max_p = int(input(">> "))
    except: max_p = 2

    while len(players) < max_p:
        print(f"[*] Waiting for player {len(players)+1}...")
        conn, addr = server.accept()
        conn.send("What's your name?".encode('utf-8'))
        p_name = conn.recv(1024).decode('utf-8').strip()
        
        balance = saved_balances.get(p_name, 5000)
        players[conn] = {"name": p_name, "money": balance, "deck": [], "folded": False}
        print(f"[+] Player '{p_name}' connected from {addr[0]} with ${balance}")

    running = True
    while running and players:
        play_one_hand(players)
        
        # Expulsión
        to_remove = []
        for conn in players:
            if players[conn]["money"] <= 0:
                print(f"[!] Kicking {players[conn]['name']} (Broke)")
                try: conn.send(json.dumps({"type": "GAME_OVER", "winner_name": "BANKRUPTCY", "winner_hand": "KICKED"}).encode('utf-8'))
                except: pass
                to_remove.append(conn)
        for conn in to_remove: del players[conn]

        if not players: break

        print("\n--- SERVER CONTROL ---")
        print("1. Next Hand | 2. Save & Exit | 3. Reset All & Exit")
        cmd = input(">> ")
        if cmd == "2":
            db = load_data()
            db.update({players[c]["name"]: players[c]["money"] for c in players})
            save_data(db)
            running = False
        elif cmd == "3":
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            running = False

    server.close()
    print("[OFFLINE] Server shut down.")

if __name__ == "__main__":
    main()