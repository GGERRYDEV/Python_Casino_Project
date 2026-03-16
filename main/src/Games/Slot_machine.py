from ..Tools.tools import master_reel_func
from ..Tools.tools import clear
from ..Tools.tools import continuee
from ..Tools.tools import prizes
from ..Tools.tools import bet
import time
import random
import pygame

# SPINNING ANIMATION
def slot_machine_spinning():
    pygame.mixer.init()
    slot1_mid, slot2_mid, slot3_mid = "", "", ""
    # LOGIC
    spinning_sound = pygame.mixer.Sound("src/Sounds/slot_machine.mp3")
    master_reel = []
    master_reel = master_reel_func(master_reel)

    n = len(master_reel) # From tools

    slot1_number = random.randint(0, n - 1)
    slot2_number = random.randint(0, n - 1)
    slot3_number = random.randint(0, n - 1)

    center = 3

    spinning_sound.play(loops=-1)

    for i in range(34):
        clear()
        slot1_number += 1
        if i > 10:
            slot2_number += 1
            if i > 20:
                slot3_number += 1
        slot1_up = master_reel[(slot1_number + 1) % n]
        slot2_up = master_reel[(slot2_number + 1) % n]
        slot3_up = master_reel[(slot3_number + 1) % n]
        slot1_mid = master_reel[slot1_number % n]
        slot2_mid = master_reel[slot2_number % n]
        slot3_mid = master_reel[slot3_number % n]
        slot1_down = master_reel[(slot1_number - 1) % n]
        slot2_down = master_reel[(slot2_number - 1) % n]
        slot3_down = master_reel[(slot3_number - 1) % n]
        print(" | 🎰 Spinning 🎰 | ")
        print(f" | {slot1_up.center(center)} {slot2_up.center(center)} {slot3_up.center(center)} |")
        print(f" | {slot1_mid.center(center)} {slot2_mid.center(center)} {slot3_mid.center(center)} |")
        print(f" | {slot1_down.center(center)} {slot2_down.center(center)} {slot3_down.center(center)} |")
        time.sleep(0.02 + (i * 0.005))
    time.sleep(0.8)
    spinning_sound.stop()
    return slot1_mid, slot2_mid, slot3_mid

# SLOT MACHINE

def slot_machine_results(slot1_mid, slot2_mid, slot3_mid):

    slot1 = slot1_mid
    slot2 = slot2_mid
    slot3 = slot3_mid

    results = [slot1, slot2, slot3]

    if "💎" in results:
        others = [s for s in results if s != "💎"]

        if others:
            best_other = max(others, key=lambda s: prizes[s])
            slot1 = best_other if slot1 == "💎" else slot1
            slot2 = best_other if slot2 == "💎" else slot2
            slot3 = best_other if slot3 == "💎" else slot3

    if slot1 == slot2 == slot3:
        multiplier = prizes[slot1]

    elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
        if slot1 == slot2 or slot1 == slot3:
            repeated = slot1
        else:
            repeated = slot2
        multiplier = prizes[repeated] // 2

    elif results[1] == "🍓":
        multiplier = 3

    else:
        multiplier = 0

    return multiplier


# START THE SLOT MACHINE

def slot_machine(player_money):
    #STARTER
    clear()
    print("Welcome to the Slot Machine!")
    print("Write return to go back to the main menu.")
    print(f"You have {player_money}")
    print("We have these prizes:")
    print("💎💎💎 (X100)")
    print("💰💰💰 (X50)")
    print("🔔🔔🔔 (X20)")
    print("🍇🍇🍇 or 🍓🍓🍓 (X10)")
    print("🍉🍉🍉 or 🍎🍎🍎 (X5)")
    print("🥝🥝🥝 or 🍋🍋🍋 (X3)")
    print("🥦🥦🥦 (X2)")
    print("Diamonds 💎 are Wildcards.")
    print("If you get a pair you will win half the jackpot!")
    print("Get a 🍓 in the center for a x3 multiplier!")
    print(f"How much money do you want to bet?")
    print(f"You have {player_money}")
    bet_amount = input()
    if bet_amount == "return":
        return player_money
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
    while player_money > 0:
        slot1_mid, slot2_mid, slot3_mid = slot_machine_spinning()
        multiplier = slot_machine_results(slot1_mid, slot2_mid, slot3_mid)
        player_money -= bet_amount
        if multiplier != 0:
            print(f"You won {multiplier * bet_amount}€!")
            player_money = player_money + multiplier * bet_amount
        else:
            print(f"You lost {bet_amount}!")
            time.sleep(1)
        if player_money == 0:
            return player_money
        print(f"You have {player_money}")
        print("Press enter to roll again")
        print("Write return to go back to the main menu.")
        print("Write another amount to play again.")
        choice = input()
        if choice == "return":
            return player_money
        elif choice.isdigit():
            bet_amount = int(choice)

    return player_money