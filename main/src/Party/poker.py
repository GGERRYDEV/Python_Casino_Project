import time
import os
import random
import socket
import threading

deck = [
    "2♥️", "3♥️", "4♥️", "5♥️", "6♥️", "7♥️", "8♥️", "9♥️", "10♥️", "J♥️", "Q♥️", "K♥️", "A♥️",
    "2♦️", "3♦️", "4♦️", "5♦️", "6♦️", "7♦️", "8♦️", "9♦️", "10♦️", "J♦️", "Q♦️", "K♦️", "A♦️",
    "2♠️", "3♠️", "4♠️", "5♠️", "6♠️", "7♠️", "8♠️", "9♠️", "10♠️", "J♠️", "Q♠️", "K♠️", "A♠️",
    "2♣️", "3♣️", "4♣️", "5♣️", "6♣️", "7♣️", "8♣️", "9♣️", "10♣️", "J♣️", "Q♣️", "K♣️", "A♣️"
]
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}
card_suits = {
    "♥️": "hearts",
    "♦️": "diamonds",
    "♠️": "spades",
    "♣️": "clubs"
}

def setup_game(players, conexion):
    random.shuffle(deck)
    print("Welcome to Poker!")
    middle_deck = []
    for i in range(3):
        middle_deck.append(deck.pop())
    print("The middle cards are:")
    print(middle_deck)
    time.sleep(2)
    for b in range(players):
        player_deck = []
        for i in range(2):
            player_deck.append(deck.pop())
        print(f"Player {b + 1} your cards are:")
        print(player_deck)
        time.sleep(2)
    detect_hand(player_deck, middle_deck)

def detect_hand(player_deck, middle_deck):
    full_deck = player_deck + middle_deck
    hand_values = []
    hand_suits = []
    for card in full_deck:
        value = card[:-2]
        suit = card[-2:]
        hand_values.append(value)
        hand_suits.append(suit)
    print (hand_values)
    print (hand_suits)
    for suit in hand_suits:
        if f"A{suit}" in full_deck and f"K{suit}" in full_deck and f"Q{suit}" in full_deck and f"J{suit}" in full_deck and f"10{suit}" in full_deck:
            print("Player has a royal flush!")
setup_game(1, None)