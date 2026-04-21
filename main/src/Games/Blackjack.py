from ..Tools.tools import bet
from ..Tools.tools import deck
from ..Tools.tools import card_values
from ..Tools.tools import continuee
from ..Tools.tools import clear
import pygame
import random
import time
pygame.mixer.init()

def blackjack_checker(value_dealer_deck, value_player_deck):
    if value_dealer_deck > 21:
        print("You won!")
        win = "player"
    elif value_player_deck > 21:
        print("Dealer won!")
        win = "dealer"
    elif value_dealer_deck == value_player_deck:
        print("It's a tie!")
        win = "tie"
    elif value_dealer_deck > value_player_deck:
        print("Dealer won!")
        win = "dealer"
    elif value_dealer_deck < value_player_deck:
        print("You won!")
        win = "player"
    else:
        win = ""
    return win

def blackjack_values(player_deck, dealer_deck, hide):
    if hide:
        clear()
        value_player_deck = 0
        value_dealer_deck = 0
        for i in range(len(player_deck)):
            value_player = card_values[player_deck[i]]
            value_player_deck += value_player
        value_dealer = card_values[dealer_deck[0]]
        value_dealer_deck += value_dealer
        full_player_deck = " , ".join(player_deck)
        full_dealer_deck = f"{dealer_deck[0]} , [X]"
        print(f"Player deck: {full_player_deck}. Total value: {value_player_deck}")
        print(f"Dealer deck: {full_dealer_deck}. Total value: {value_dealer_deck}")
        if value_player_deck > 21:
            return False, value_dealer_deck, value_player_deck
        else:
            return True, value_dealer_deck, value_player_deck
    else:
        value_player_deck = 0
        value_dealer_deck = 0
        for i in range(len(player_deck)):
            value_player = card_values[player_deck[i]]
            value_player_deck += value_player
        for r in range(len(dealer_deck)):
            value_dealer = card_values[dealer_deck[r]]
            value_dealer_deck += value_dealer
        full_player_deck = " , ".join(player_deck)
        full_dealer_deck = " , ".join(dealer_deck)
        print(f"Player deck: {full_player_deck}. Total value: {value_player_deck}")
        print(f"Dealer deck: {full_dealer_deck}. Total value: {value_dealer_deck}")
        return False, value_dealer_deck, value_player_deck

def blackjack(player_money):
    hit = pygame.mixer.Sound("src/Sounds/hit.mp3")
    clear()
    print("Welcome to the Blackjack!")
    bet_amount = bet(player_money)
    while player_money > 0:
        clear()
        player_deck = random.choices(deck, k=2 )
        dealer_deck = random.choices(deck, k=2 )
        hide = True
        blackjack_values(player_deck, dealer_deck, hide)
        keep_playing = True
        value_dealer_deck = 0
        value_player_deck = 0
        while keep_playing:
            print("What do you want to do?")
            print("[H]it or [S]tand?")
            choice = input()
            if choice == "H":
                hit.play()
                clear()
                player_deck.append(random.choice(deck))
                keep_playing, value_dealer_deck, value_player_deck = blackjack_values(player_deck, dealer_deck, hide)
            elif choice == "S":
                clear()
                hide = False
                keep_playing, value_dealer_deck, value_player_deck = blackjack_values(player_deck, dealer_deck, hide)
                while value_dealer_deck < 21 and value_dealer_deck < value_player_deck:
                    hit.play()
                    print("Dealer hits")
                    time.sleep(1)
                    clear()
                    dealer_deck.append(random.choice(deck))
                    keep_playing, value_dealer_deck, value_player_deck = blackjack_values(player_deck, dealer_deck, hide)
        win = blackjack_checker(value_dealer_deck, value_player_deck)
        if win == "dealer":
            print(f"You lost {bet_amount}")
            player_money -= bet_amount
        elif win == "player":
            print(f"You won {bet_amount * 2}")
            player_money += bet_amount
        continuee()
        clear()
        if player_money == 0:
            return player_money
        print(f"You have {player_money}")
        print("Press enter to play again")
        print("Write return to go back to the main menu.")
        print("Write another amount to play again.")
        choice = input()
        if choice == "return":
            return player_money
        elif choice.isdigit():
            if bet_amount <= 0:
                print("Please enter a valid amount")
                print(f"You have {player_money}")
            elif bet_amount > player_money:
                print("You don't have enough money")
                print(f"You have {player_money}")
            elif player_money == 0:
                return player_money
            else:
                bet_amount = int(choice)
        if bet_amount > player_money:
            bet_amount = player_money
    return player_money