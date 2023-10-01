
N_CARDS = 48  # no jacks
N_DECKS = 2
SPOT_ENUMS = {
    0: "empty",
    1: "player 1",
    2: "player 2",
    3: "wild",
}
CARDS = {
    "number": range(N_CARDS / 4),
    "name": ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "queen", "king", "ace"],
    "suit": ["Spades", "Hearts", "Clubs", "Diamonds"],
}
import torch
import numpy as np

def board():
    
    flat_state = torch.zeros(N_CARDS * N_DECKS)
    
    for i in range(4):
        flat_state[ (N_CARDS * N_DECKS / 4) * i] = 3 
    
    # build an N x M mat of zeros
    mat_state = torch.zeros(N_DECKS, N_CARDS)
    
    

def ind2card(ind):
    return ind % N_CARDS

def card2ind(card):
    pass

def actions(board, hand, player):
    pass

def main(): 
    print("Hello World")



if __name__ == '__main__':
    main()