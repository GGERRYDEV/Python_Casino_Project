# Clear
import random
import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# BLACKJACK

deck = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
] * 4

card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

# Roulette

colors_roulette = [
    (0, "🟩"), (1, "🟥"), (2, "⬛"), (3, "🟥"), (4, "⬛"), (5, "🟥"), (6, "⬛"), (7, "🟥"), (8, "⬛"), (9, "🟥"),
    (10, "⬛"), (11, "⬛"), (12, "🟥"), (13, "⬛"), (14, "🟥"), (15, "⬛"), (16, "🟥"), (17, "⬛"), (18, "🟥"),
    (19, "🟥"), (20, "⬛"), (21, "🟥"), (22, "⬛"), (23, "🟥"), (24, "⬛"), (25, "🟥"), (26, "⬛"), (27, "🟥"),
    (28, "⬛"), (29, "⬛"), (30, "🟥"), (31, "⬛"), (32, "🟥"), (33, "⬛"), (34, "🟥"), (35, "⬛"), (36, "🟥")
]

choices = ["Red", "Black", "Even", "Odd", "High", "Low", "Green", "Number", "1 Column", "2 Column", "3 Column"]

def master_reel_func(master_reel):
    for symbol, weight in reel_config.items():
        master_reel.extend([symbol] * weight)
        random.shuffle(master_reel)
    return master_reel

# SLOT MACHINE

reel_config = {
    "💎": 3,
    "💰": 4,
    "🔔": 5,
    "🍇": 7,
    "🍓": 10,
    "🍉": 12,
    "🍎": 13,
    "🥝": 15,
    "🍋": 15,
    "🥦": 20
}

prizes = {
    "💎": 100,
    "💰": 50,
    "🔔": 20,
    "🍇": 10,
    "🍓": 10,
    "🍉": 5,
    "🍎": 5,
    "🥝": 3,
    "🍋": 3,
    "🥦": 2
}

# Ask for bet amount

def bet(player_money):
    print(f"How much money do you want to bet?")
    print(f"You have {player_money}")
    bet_amount = input()
    if bet_amount == "return":
        return bet_amount
    elif bet_amount == "":
        bet_amount = 0
        while bet_amount <= 0 or bet_amount > player_money:
            if bet_amount <= 0:
                print("Please enter a valid amount")
                print(f"You have {player_money}")
            else:
                print("You don't have enough money")
                print(f"You have {player_money}")
            bet_amount = int(input())
    else:
        bet_amount = int(bet_amount)
        while bet_amount <= 0 or bet_amount > player_money:
            if bet_amount <= 0:
                print("Please enter a valid amount")
                print(f"You have {player_money}")
            else:
                print("You don't have enough money")
                print(f"You have {player_money}")
            bet_amount = int(input())
    return bet_amount

# ASK FOR CONTINUE

def continuee():
    print("Press any key to continue")
    input()
