from ..Tools.tools import bet
from ..Tools.tools import clear
from ..Tools.tools import colors_roulette
from ..Tools.tools import choices
from ..Tools.tools import continuee
import time
import random

def spinning():
    roulette_number = 0
    roulette_color = ""
    for i in range(36):
        clear()
        roulette_number, roulette_color = random.choice(colors_roulette)
        print("🎰Spinning...🎰")
        print(f"🎲 {roulette_number} {roulette_color} 🎲")
        time.sleep(i * 0.005)
    return roulette_number, roulette_color

def result_roulette(choice, number_choice, roulette_number, roulette_color):

    # Default multiplier is 0 (player loses)

    multiplier = 0

    # Convert emoji to text color
    if roulette_color == "🟥":
        current_color = "Red"
    elif roulette_color == "⬛":
        current_color = "Black"
    else:
        current_color = "Green"

    # Check Number or Green
    if choice == "Number" and roulette_number == number_choice:
        multiplier = 36
    elif choice == "Green" and current_color == "Green":
        multiplier = 36

    # Check Colors (Red or Black)
    elif choice == current_color:
        multiplier = 2

    # Check specific bets (Only if number is NOT 0)
    elif roulette_number != 0:
        # Even or Odd logic
        if choice == "Even" and roulette_number % 2 == 0:
            multiplier = 2
        elif choice == "Odd" and roulette_number % 2 != 0:
            multiplier = 2

        # High or Low logic
        elif choice == "Low" and 1 <= roulette_number <= 18:
            multiplier = 2
        elif choice == "High" and 19 <= roulette_number <= 36:
            multiplier = 2

        # Column logic
        elif choice == "1 Column" and 1 <= roulette_number <= 12:
            multiplier = 3
        elif choice == "2 Column" and 13 <= roulette_number <= 24:
            multiplier = 3
        elif choice == "3 Column" and 25 <= roulette_number <= 36:
            multiplier = 3

    return multiplier


def roulette(player_money):
    bet_amount = -1
    number_choice = -1
    while player_money > 0:
        clear()
        print("Welcome to the Roulette!")
        print(f"You have {player_money}")
        print("You can choose between:")
        print("If you want to return to the main menu write return")
        print("Number (X36)")
        print("Green (X36)")
        print("1 Column (1-12, X3)")
        print("2 Column (13-24, X3)")
        print("3 Column (25-36, X3)")
        print("Red (X2)")
        print("Black (X2)")
        print("Even (X2)")
        print("Odd (X2)")
        print("High (19-36, X2)")
        print("Low (1-18, X2)")
        choice = input()
        if choice == "return":
            return player_money
        elif choice == "Number":
            print("Choose a number between 0 and 36")
            number_choice = int(input())
            while number_choice < 0 or number_choice > 36:
                print("Please choose between 0 and 36")
                number_choice = int(input())
            bet_amount = bet(player_money)
        elif choice in choices:
            bet_amount = bet(player_money)
            number_choice = 37
        else:
            print("Unrecognized option")
            time.sleep(1)
            continue
        roulette_number, roulette_color = spinning()
        multiplier = result_roulette(choice, number_choice, roulette_number, roulette_color)
        if multiplier == 0:
            print(f"You lost {bet_amount}!")
            player_money = player_money - bet_amount
        else:
            print(f"You won {bet_amount * multiplier}!")
            player_money = player_money - bet_amount
            player_money = player_money + bet_amount * multiplier

        continuee()
    return player_money


