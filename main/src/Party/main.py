from ..Tools.tools import bet
from ..Tools.tools import deck
from ..Tools.tools import card_values
from ..Tools.tools import continuee
from ..Tools.tools import clear
import os
import pygame
import random
import time
import socket
import threading

def party(player_money):
    print("Welcome to the Party game!")
    print("This game is designed for multiple players. You can play with your friends and have fun together!")
    print("Each player will start with the same amount of money")
    print("For the moment we only have poker, but we will add more games in the future")
    print("To play with your friends, you can either host a game or join a game")
    print("If you want to host a game, type 'host'")
    print("If you want to join a game, type 'join'")
    choice = input()
    if choice == "host":
        from .host import host
        host(player_money)
    elif choice == "join":
        from .player import player
        player(player_money)
    else:
        print("Please enter a valid input")
        time.sleep(1)
        return party(player_money)