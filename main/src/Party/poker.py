import time
import os
import random
import json

# GAME SETUP
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

# --- GAME ENGINE FUNCTIONS ---

def start_deal(players):
    """Shuffles and deals 2 cards to each player and prepares the board."""
    current_deck = deck[:] 
    random.shuffle(current_deck)
    print("Deck shuffled!")

    # Prepare 5 cards for the community board
    middle_deck = [current_deck.pop() for _ in range(5)]

    # Deal private hands
    for conexion in players:
        card1 = current_deck.pop()
        card2 = current_deck.pop()
        players[conexion]["deck"] = [card1, card2]
        
        data = {
            "type": "HAND",
            "player_name": players[conexion]['name'],
            "cards": [card1, card2],
            "message": f"You received {card1} and {card2}"
        }
        
        message_json = json.dumps(data) + "\n"
        conexion.send(message_json.encode('utf-8'))
    
    return players, middle_deck

def update_board(players, middle_deck, round_level):
    """Sends the current community cards (Flop, Turn, River) to all players."""
    cards_to_show = [3, 4, 5]
    visible_cards = middle_deck[:cards_to_show[round_level]]
    
    data = {
        "type": "UPDATE_BOARD",
        "cards": visible_cards,
        "round": round_level
    }
    
    msg = (json.dumps(data) + "\n").encode('utf-8')
    for conn in players:
        conn.send(msg)

# --- HAND DETECTION LOGIC ---

def detect_hand(player_deck, middle_deck):
    """Analyzes 2 private cards + current board cards to find the best hand."""
    if not middle_deck:
        return "High_Card", 0

    full_deck = player_deck + middle_deck
    hand_suits = [card[-2:] for card in full_deck]
    processed_cards = []
    
    for card in full_deck:
        value_text = card[:-2]
        suit = card[-2:]
        processed_cards.append([card_values[value_text], suit])
    
    processed_cards.sort()
    processed_cards_values = [card[0] for card in processed_cards]
    processed_cards_values_unic = sorted(list(set(processed_cards_values)))

    # 1. ROYAL FLUSH
    for suit in set(hand_suits):
        royal_values = [10, 11, 12, 13, 14]
        if all([val, suit] in processed_cards for val in royal_values):
            return "Royal_Flush", 14

    # 2. STRAIGHT FLUSH
    for suit in set(hand_suits):
        suit_nums = sorted([c[0] for c in processed_cards if c[1] == suit])
        if len(suit_nums) >= 5:
            for i in range(len(suit_nums) - 4):
                if suit_nums[i+4] == suit_nums[i] + 4:
                    return "Straight_Flush", suit_nums[i+4]

    # 3. POKER (Four of a Kind)
    for value in set(processed_cards_values):
        if processed_cards_values.count(value) == 4:
            return "Poker", value
        
    # 4. TRIOS AND PAIRS COUNTER
    trios = [v for v in set(processed_cards_values) if processed_cards_values.count(v) == 3]
    pairs = [v for v in set(processed_cards_values) if processed_cards_values.count(v) == 2]
    trios.sort(reverse=True)
    pairs.sort(reverse=True)

    # 5. FULL HOUSE
    if (trios and pairs) or len(trios) > 1:
        return "Full_House", trios[0]

    # 6. FLUSH
    for suit in set(hand_suits):
        if hand_suits.count(suit) >= 5:
            flush_cards = [c[0] for c in processed_cards if c[1] == suit]
            return "Flush", max(flush_cards)

    # 7. STRAIGHT
    for i in range(len(processed_cards_values_unic) - 1, 3, -1):
        if processed_cards_values_unic[i] == processed_cards_values_unic[i-4] + 4:
            return "Straight", processed_cards_values_unic[i]

    # 8. THREE OF A KIND
    if trios:
        return "Three_of_a_Kind", trios[0]

    # 9. TWO PAIR
    if len(pairs) >= 2:
        return "Two_Pair", pairs[0] 

    # 10. PAIR
    if pairs:
        return "Pair", pairs[0]

    # 11. HIGH CARD
    return "High_Card", processed_cards_values_unic[-1]

# --- WINNER CALCULATION ---

hand_rankings = {
    "Royal_Flush": 10,
    "Straight_Flush": 9,
    "Poker": 8,
    "Full_House": 7,
    "Flush": 6,
    "Straight": 5,
    "Three_of_a_Kind": 4,
    "Two_Pair": 3,
    "Pair": 2,
    "High_Card": 1
}

def winer(player_results):
    """Sorts players by hand rank, then high card value, and returns the winner."""
    # player_results: [("Pair", 14, "Name"), ...]
    player_results.sort(key=lambda x: (hand_rankings.get(x[0], 0), x[1]), reverse=True)
    winner = player_results[0]
    print(f"\n🏆 THE WINNER IS: {winner[2]} with a {winner[0].replace('_', ' ')}!")
    return winner