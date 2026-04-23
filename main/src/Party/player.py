import socket
import threading
import time
import os
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP Setup - Change to the Host's IP if not playing on the same machine
ip = "127.0.0.1" 
try:
    client.connect((ip, 5555))
except Exception as e:
    print(f"Could not connect to server: {e}")
    exit()

# Initial Handshake
question = client.recv(1024).decode('utf-8')
name = input(f"{question}\n")
client.send(name.encode('utf-8'))

def receive_message():
    while True:
        try:
            raw_data = client.recv(4096).decode('utf-8')
            if not raw_data:
                print("\n[DISCONNECTED] Server closed.")
                break
                
            messages = raw_data.split("\n")
            
            for msg in messages:
                if not msg.strip(): 
                    continue
                
                data = json.loads(msg)
                
                # --- CLEAR AND RE-DRAW INTERFACE ---
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # 1. SPECIAL CASE: GAME OVER
                if data["type"] == "GAME_OVER":
                    print("\n" + "🏆" * 20)
                    print(f"  WINNER: {data['winner_name'].upper()}")
                    print(f"  HAND:   {data['winner_hand'].replace('_', ' ')}")
                    print("🏆" * 20)
                    input("\nPress Enter to continue...")
                    continue

                # --- 2. REGULAR INTERFACE DRAWING ---
                print("="*50)
                print(f" PLAYER: {name.upper()} | BALANCE: ${data.get('money', '---')}")
                print("="*50)
                
                # Handle Board display
                board = data.get("board", [])
                if data["type"] == "UPDATE_BOARD": 
                    board = data.get("cards", [])
                print(f"\n BOARD: {' | '.join(board) if board else '[ Pre-Flop ]'}")
                
                # Handle Private Hand display
                hand = data.get("hand", [])
                if data["type"] == "HAND": 
                    hand = data.get("cards", [])
                if hand:
                    print(f" YOUR HAND: {hand[0]}  {hand[1]}")
                
                # Show current hand strength (e.g., Pair, Trio, Flush)
                if "current_hand_type" in data:
                    print(f" STRENGTH:  {data['current_hand_type'].replace('_', ' ')}")
                
                print("-" * 50)

                # --- 3. INPUT LOGIC ---
                
                # Normal Turn
                if data["type"] == "ACTION_REQUIRED":
                    print(f"\n[!] {data['message']}")
                    choice = input(">> Action (Check/Raise/Fold): ").strip().lower()
                    client.send((json.dumps({"action": choice}) + "\n").encode('utf-8'))
                
                # Asking for specific Raise amount
                elif data["type"] == "ASK_AMOUNT":
                    print(f"\n[?] {data['message']}")
                    amount = input(">> Enter amount to raise: ")
                    # If user enters nothing or non-digit, default to 0 to avoid crash
                    if not amount.isdigit():
                        amount = "0"
                    client.send((json.dumps({"amount": amount}) + "\n").encode('utf-8'))

        except Exception as e:
            print(f"\nError receiving data: {e}")
            break

if __name__ == "__main__":
    receive_message()