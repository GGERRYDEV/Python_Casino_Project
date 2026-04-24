import socket
import threading
import time
import os
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP Setup - Change to the Host's IP if needed
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
                
                # --- CLEAR SCREEN ---
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # 1. SPECIAL CASE: GAME OVER (WINNER ANNOUNCEMENT)
                if data["type"] == "GAME_OVER":
                    print("\n" + "🏆" * 20)
                    print(f"  WINNER: {data['winner_name'].upper()}")
                    print(f"  HAND:   {data['winner_hand'].replace('_', ' ')}")
                    print("🏆" * 20)
                    input("\nPress Enter to start a new round...")
                    continue

                # --- 2. MAIN INTERFACE DRAWING ---
                print("="*55)
                print(f" PLAYER: {name.upper()} | BALANCE: ${data.get('money', '---')}")
                print(f" TOTAL POT: ${data.get('pot', 0)}")
                print("="*55)
                
                board = data.get("board", [])
                print(f"\n COMMUNITY CARDS: {' | '.join(board) if board else '[ Pre-Flop ]'}")
                
                hand = data.get("hand", [])
                if hand:
                    print(f" YOUR HAND: {hand[0]}  {hand[1]}")
                
                if "current_hand_type" in data:
                    print(f" CURRENT RANK: {data['current_hand_type'].replace('_', ' ')}")
                
                print("-" * 55)

                # --- 3. PLAYER ACTIONS ---
                
                if data["type"] == "ACTION_REQUIRED":
                    to_call = data.get('to_call', 0)
                    if to_call > 0:
                        print(f"[!] You must bet ${to_call} to stay in (Call/Raise).")
                    else:
                        print("[!] No active bets. You can Check for free.")

                    print(f"\n[TURN] {data.get('message', 'It is your turn')}")
                    choice = input(">> Action (Check/Raise/Fold): ").strip().lower()
                    client.send((json.dumps({"action": choice}) + "\n").encode('utf-8'))

                elif data["type"] == "ASK_AMOUNT":
                    print(f"\n[?] {data.get('message', 'How much do you want to raise?')}")
                    amount = input(">> Extra amount to add: ")
                    if not amount.isdigit(): 
                        amount = "0"
                    client.send((json.dumps({"amount": amount}) + "\n").encode('utf-8'))

                elif data["type"] == "WAIT_TURN":
                    print("\n[WAITING] Other player is acting. Screen will update soon...")

        except Exception as e:
            print(f"\nError receiving data: {e}")
            break

if __name__ == "__main__":
    receive_message()