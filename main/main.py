# Import libraries

from src.src import *

# Start the game

def start_casino(player_money):
    while player_money > 0:
        clear()
        print("Welcome to the python casino!")
        print(f"You have {player_money}")
        print("We have these games:")
        print("1. Roulette")
        print("2. Blackjack")
        print("3. Dice")
        print("4. Slot Machine")
        print("5. Loop ( For loop games ).")
        print("You can choose the game with the number or the name of the game")
        print("If you want to exit the casino, type 'exit' at any time")
        game_choice = input()
        if game_choice == "1" or game_choice == "Roulette":
            roulette()
        elif game_choice == "2" or game_choice == "Blackjack":
            blackjack()
        elif game_choice == "3" or game_choice == "Dice":
            player_money = dice(player_money)
        elif game_choice == "4" or game_choice == "Slot Machine":
            slot_machine()
        elif game_choice == "5" or game_choice == "Loop":
             loop()
        elif game_choice == "exit":
            exit()
        else:
            print("Please enter a valid input")
            time.sleep(1)



if __name__ == "__main__":
    start_casino(5000)
