# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:50:09 2020

@author: Daria
"""
import random
import numpy as np
#import matplotlib.pyplot as plt
random.seed(1)

def create_board():
    board = np.zeros((3,3), dtype=int)    
    return board

player = 0
#places a chess if it is empty
def place(board, player, position):
    if board[position]== 0:
        board [position] = player     
    return board

#checks available options for placement, returns a list of coordinates
def possibilities(board):
    return list(zip(*np.where(board == 0)))

#randomly places a chess
def random_place(board, player):
    selections = possibilities(board)
    if len(selections) > 0:
        selection = random.choice(selections)
        place(board, player, selection)
    return board

#checks rows for winner
def row_win(board, player):
    if np.any(np.all(board==player, axis=1)): # this checks if any row contains all positions equal to player.
        return True
    else:
        return False          

#checks columns for winner    
def col_win(board, player):
    if np.any(np.all(board==player, axis=0)): # this checks if any column contains all positions equal to player
        return True
    else:
        return False
    
#checks diagonals                   
def diag_win(board, player):
    if np.all(np.diag(board)==player) or np.all(np.diag(np.fliplr(board))==player):
        # np.diag returns the diagonal of the array
        # np.fliplr rearranges columns in reverse order
        return True
    else:
        return False

#checks the whole board
def evaluate(board):
    winner = 0
    for player in [1, 2]:
        if row_win(board,player) or col_win(board, player) or diag_win(board, player)==True:
            winner = player            
        elif np.all(board != 0) and winner == 0:
            winner = -1
    #print ('winner:', winner)
    return winner

#plays the whole game
def play_game():    
    board = create_board() 
    result = 0
    while result == 0:    
        for player in [1, 2]:
            random_place(board, player)              
            #print ('Step:', 'player', player, '\n', board)
            result = evaluate(board)              
            #print('result:', result)
            if result !=0:                  
                break
    return result

#counts results and prints them
results = [play_game() for i in range(1000)]
print(results.count(1))

def play_strategic_game():
    board = create_board()
    place(board, 1, (1, 1))
    result = 0
    while result == 0:        
        for player in [2, 1]:            
            random_place(board, player)              
            #print ('Step:', 'player', player, '\n', board)
            result = evaluate(board)              
            #print('result:', result)
            if result !=0:                  
                break
    return result
#counts results and prints them
results_strategic = [play_strategic_game() for i in range(1000)]
print(results_strategic.count(1))   



    
    
    

