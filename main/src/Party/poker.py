import time
import os
import random
import socket
import threading
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    clear()
    random.shuffle(deck)
    print("Welcome to Poker!")
    middle_deck = []
    for i in range(5):
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
    processed_cards = []
    for card in full_deck:
        value_text = card[:-2]
        suit = card[-2:]
        hand_values.append(value_text)
        hand_suits.append(suit)
        value_number = card_values[value_text]
        processed_cards.append([value_number, suit])
    processed_cards.sort()
    processed_cards_values = []
    processed_cards_suits = []
    processed_cards_values = []
    for cards in processed_cards:
        processed_cards_values.append(cards[0])
    processed_cards_values_unic = list(set(processed_cards_values))
    processed_cards_values_unic.sort()
    # ROYAL FLUSH
    
    for suit in hand_suits:
        if f"A{suit}" in full_deck and f"K{suit}" in full_deck and f"Q{suit}" in full_deck and f"J{suit}" in full_deck and f"10{suit}" in full_deck:
            print("Player has a royal flush!")
            return "Royal_Flush"
        
    # STRAIGHT FLUSH
    
    for suit in set(hand_suits):
        numbers_of_suit = [] 
        
        for card in processed_cards:
            if card[1] == suit:
                numbers_of_suit.append(card[0])
                
        if len(numbers_of_suit) >= 5:
            numbers_of_suits_unic = list(set(numbers_of_suit))
            numbers_of_suits_unic.sort() 
            
            for number in numbers_of_suits_unic:
                if (number + 1) in numbers_of_suits_unic and (number + 2) in numbers_of_suits_unic and (number + 3) in numbers_of_suits_unic and (number + 4) in numbers_of_suits_unic:
                    print("Player has a straight flush!")
                    return "Straight_Flush"
    
    # POKER
    
    for vaule in set(hand_values):
        if hand_values.count(vaule) == 4:
            print("Player has a poker")
            return "Poker"
        
    # FULL HOUSE and detecting trios and pairs

    trios = 0
    pairs = 0
    processed_cards_values = []
    for cards in processed_cards:
        processed_cards_values.append(cards[0])
    for number in set(processed_cards_values):
        quantity = processed_cards_values.count(number)
        
        if quantity == 3:
            trios += 1
        elif quantity == 2:
            pairs += 1

    if (trios == 1 and pairs >= 1) or (trios == 2):
        print("Player has a full house!")
        return "Full_House"
    
    # FLUSH

    for suit in set(hand_suits):
        if hand_suits.count(suit) >= 5:
            print("Player has a flush!")
            return "Flush"
        
    # STRAIGHT

    for number in processed_cards_values_unic:
        if (number + 1) in processed_cards_values_unic and (number + 2) in processed_cards_values_unic and (number + 3) in processed_cards_values_unic and (number + 4) in processed_cards_values_unic:
            print("Player has a straight!")
            return "Straight"
        
    # TRIO 

    if trios >= 1:
        print("Player has a trio")
        return "Trio"
    
    # DOUBLE PAIR

    if pairs >= 2:
        print("Player has a double pair")
        return 'Double_Pair'
    
    # PAIR

    if pairs == 1:
        print('Player has a pair')
        return 'Pair'
    
    # HIGH CARD

    high_card = processed_cards_values_unic[-1]
    print(high_card)
    print('The player has a high card')
    return 'High_Card'

setup_game(1, None)