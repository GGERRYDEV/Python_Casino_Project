from ..Tools.tools import bet
from ..Tools.tools import clear
from ..Tools.tools import continuee
import random
import time
import pygame
pygame.mixer.init()

def dice(player_money):
    while player_money > 0:
        clear()
        print("Welcome to the Dice game")
        print("You can choose a number between 1 and 6")
        print("If you hit the correct number you will get your money multiplied by 5")
        print("If you want to return to the main menu write return")
        bet_amount = bet(player_money)
        if bet_amount == "return":
            return player_money
        else:
            player_money = int(player_money)
            print("Please enter a number between 1 and 6")
            number_choice = int(input())
            while number_choice not in range(1, 6):
                print("Please enter a number between 1 and 6")
                number_choice = int(input())
            random_number = random.randint(1, 6)
            dice_sound = pygame.mixer.Sound("src/Sounds/dice.mp3")
            dice_sound.play()
            time.sleep(1)
            if random_number == number_choice:
                won_money = bet_amount * 4
                print(f"You won {won_money}€")
                print(f"The number was {random_number} and your number was {number_choice}")
                player_money = won_money + player_money
                continuee()
            else:
                print(f"You lost {bet_amount}")
                print(f"The number was {random_number} and your number was {number_choice}")
                player_money = player_money - bet_amount
                continuee()

            clear()
    return player_money
