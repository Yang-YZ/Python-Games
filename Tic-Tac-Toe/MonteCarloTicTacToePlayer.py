"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player): 
    """
    play a game starting with the given player by making 
    # random moves, alternating between players. 
    # The function should return when the game is over. 
    # The modified board will contain the state of the game, 
    # so the function does not return anything.
    """
    while board.check_win() == None:
        print board
        empty_squares = board.get_empty_squares()
        row_col = random.choice(empty_squares)
        print row_col
        board.move(row_col[0], row_col[1], player)
        player = provided.switch_player(player)    
    print board
    print board.check_win()

def mc_update_scores(scores, board, player):
    """
    takes a grid of scores (a list of lists) 
    # with the same dimensions as the Tic-Tac-Toe board, 
    # a board from a completed game, and which player the machine player is. 
    # The function should score the completed board and update the scores grid. 
    # not return anything.
    
    # If the current player (the player for which your code is currently selecting a move) won the game, 
    # each square that matches the current player should get a positive score 
    # (corresponding to SCORE_CURRENT in the template
    # each square that matches the other player should get a negative score 
    # (corresponding to -SCORE_OTHER in the template
    # Conversely, if the current player lost the game, 
    # each square that matches the current player should get a negative score (-SCORE_CURRENT)
    # each square that matches the other player should get a positive score (SCORE_OTHER). 
    # All empty squares should get a score of 0.
    """
    
    current_player = player
    other_player = provided.switch_player(current_player)
    print scores    
    if board.check_win() == current_player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if current_player == board.square(row, col):
                    scores[row][col] += SCORE_CURRENT
                elif other_player == board.square(row, col):
                    scores[row][col] -= SCORE_OTHER
    elif board.check_win() == other_player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if current_player == board.square(row, col):
                    scores[row][col] -= SCORE_CURRENT
                elif other_player == board.square(row, col):
                    scores[row][col] += SCORE_OTHER
    print board
    print scores
    

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    # The function should find all of the empty squares with the maximum score 
    # and randomly return one of them as a (row, column) tuple. 
    # It is an error to call this function with a board that has no empty squares (there is no possible next move), 
    # so your function may do whatever it wants in that case. 
    # The case where the board is full will not be tested.
    """
    empty_squares = board.get_empty_squares()
    print empty_squares
    max_val = None
    for row_col in empty_squares:        
        value = scores[row_col[0]][row_col[1]]
        print row_col
        print value
        if max_val is None or value > max_val:
            max_indices = [row_col]
            max_val = value
        elif value == max_val:
            max_indices.append(row_col)
    print max_val, max_indices
    print random.choice(max_indices)
    return random.choice(max_indices)

def mc_move(board, player, trials):    
    """
    This function takes a current board, which player the machine player is, 
    # and the number of trials to run. 
    # The function should use the Monte Carlo simulation described above 
    # to return a move for the machine player in the form of a (row, column) tuple. 
    # Be sure to use the other functions you have written!
    
    # Repeat for the desired number of trials: 
    # A. Set the current board to be board. 
    # B. Play an entire game on this board by just randomly choosing a move for each player. 
    # C. Score the resulting board. 
    # D. Add the scores from 2C to the running total of all scores.
    # To select a move, randomly choose one of the empty squares on the board that has the maximum score.
    """
    scores = [[0 for dummy_col in range(board.get_dim())]
                           for dummy_row in range(board.get_dim())]
    print scores
    for dummy_round in range(trials):
        board_round = board.clone()
        mc_trial(board_round, player)
        mc_update_scores(scores, board_round, player)
    print get_best_move(board, scores)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
