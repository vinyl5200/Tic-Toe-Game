"""Assignment 3"""

import copy

def make_move(grid, player, x, y):
      grid[x][y] = player
      return grid

def get_empty_locations(grid):
      empty_loc = []                                    ## Stores list of empty locations

      for i in range(len(grid)):
        for j in range(len(grid[0])):
          if grid[i][j] == ' ':
            empty_loc.append((i, j))
      return empty_loc

def minimax_algorithm(grid, max_player, min_player, max_player_turn):
      status = utility(grid, max_player, min_player)
      # print(f"Status = {status}")
      if status:
        return status

      empty_loc = get_empty_locations(grid)

      if len(empty_loc) == 0:
        return utility(grid, max_player, min_player)

      if max_player_turn:
        alpha = -2                                     ## possible alpha values will be -1, 0, 1
        for loc in empty_loc:
          updated_grid = copy.deepcopy(grid)
          updated_grid = make_move(updated_grid, max_player, loc[0], loc[1])
          # print_grid(updated_grid)
          possible_score = minimax_algorithm(updated_grid, max_player, min_player, not max_player_turn)
          # print(f"Possible score = {possible_score}")
          alpha = max(alpha, possible_score)
        return alpha

      else:
        # print("Original grid:\n")
        # print_grid(grid)
        beta = 2                                     ## possible beta values will be -1, 0, 1
        for loc in empty_loc:
          updated_grid = copy.deepcopy(grid)
          updated_grid = make_move(updated_grid, min_player, loc[0], loc[1])
          # print_grid(updated_grid)
          possible_score = minimax_algorithm(updated_grid, max_player, min_player, not max_player_turn)
          # print(f"Possible score = {possible_score}")
          beta = min(beta, possible_score)
        return beta

def get_best_move(grid, max_player, min_player, max_player_turn):
    x, y = -1, -1
    player = max_player
    empty_loc = get_empty_locations(grid)
    value = 0

    if max_player_turn:
      player = max_player
      value = -2                                   ## possible values will be -1, 0, 1

    else:
      player = min_player
      value = 2

    for loc in empty_loc:
      updated_grid = copy.deepcopy(grid)
      updated_grid = make_move(updated_grid, player, loc[0], loc[1])
      possible_score = minimax_algorithm(updated_grid, max_player, min_player, not max_player_turn)
      if max_player_turn and (possible_score > value):
        value = possible_score
        x = loc[0]
        y = loc[1]

      elif (not max_player_turn) and (possible_score < value):
        value = possible_score
        x = loc[0]
        y = loc[1]

    return (x, y)


def utility(grid, max_player, min_player):

    ## Check for each row
    for i in range(len(grid)):
      player = grid[i][0]
      winner_found = True
      for j in range(len(grid[0])):
        if grid[i][j] != player:
          winner_found = False
          break

      if winner_found and player != ' ':
        return 1 if (player == max_player) else -1

    ## Check for each column
    for j in range(len(grid[0])):
      player = grid[0][j]
      winner_found = True
      for i in range(len(grid)):
        if grid[i][j] != player:
          winner_found = False
          break

      if winner_found and player != ' ':
        return 1 if (player == max_player) else -1

    ## Check for top left to bottom right diagonal
    player = grid[0][0]
    winner_found = True
    for i in range(len(grid)):
      if grid[i][i] != player:
        winner_found = False
        break

    if winner_found and player != ' ':
      return 1 if (player == max_player) else -1

    ## Check for top right to bottom left diagonal
    val = len(grid[0]) - 1
    player = grid[0][val]
    winner_found = True
    for i in range(len(grid)):
      if grid[i][val-i] != player:
        winner_found = False
        break

    if winner_found and player != ' ':
      return 1 if (player == max_player) else -1

    ## Return 0 in case of a draw
    return 0

def print_grid(grid):
  for i in range(len(grid)):
      for j in range(len(grid[0])):
        if grid[i][j] == ' ':
          print("_", end = " ")

        else:
          print(grid[i][j], end = " ")
      print("\n")

if __name__ == '__main__':
    grid = [[' ', ' ', ' '],                     ## initially all grid cells are empty
            [' ', ' ', ' '],
            [' ', ' ', ' ']]
    # grid2 = [[' ', 'O', 'X'], [' ', 'X', ' '], ['O', ' ', ' ']]
    # grid3 = [['X', 'X', 'O'],
    #         ['O', 'O', ' '],
    #         ['X', ' ', ' ']]
    # grid4 = [['X', 'X', 'O'],
    #         ['O', 'O', ' '],
    #         [' ', 'X', ' ']]


    max_player = 'X'
    min_player = 'O'

    max_player_turn = True
    score = 0

    choice = input("Which of the following do you want?\n1. Play game with computer\n2. Let two computers play with each other\nEnter your choice : ")
    if choice == '1':
      print("Original grid:")
      print_grid(grid)
      empty_loc = get_empty_locations(grid)

      while(len(empty_loc)):
        if score:
          break

        if max_player_turn:                                                    ## We have assumed that user is putting 'X'
           print("Your turn ('X') : ")
           while True:
            x = int(input("Enter row number (0/1/2) : "))
            y = int(input("Enter column number (0/1/2) : "))

            if grid[x][y] != ' ':
              print("Invalid move!")

            else:
              break

           make_move(grid, max_player, x, y)

        else:
           print("Computer's turn ('O'): ")
           (x, y) = get_best_move(grid, max_player, min_player, max_player_turn)
           make_move(grid, min_player, x, y)

        max_player_turn = not max_player_turn
        print("Updated grid :")
        print_grid(grid)

        check_score = utility(grid, max_player, min_player)
        if check_score:
          break

        empty_loc = get_empty_locations(grid)


    else:
      print("Original grid:")
      print_grid(grid)
      empty_loc = get_empty_locations(grid)

      while(len(empty_loc)):

        if score:
          break

        if max_player_turn:                                                    ## We have assumed that computer 1 is putting 'X' on behalf of you
           print("Computer 1's turn ('X'): ")
           (x, y) = get_best_move(grid, max_player, min_player, max_player_turn)
           make_move(grid, max_player, x, y)

        else:                                                                  ## We have assumed that computer 2 is putting 'O'
           print("Computer 2's turn ('O'): ")
           (x, y) = get_best_move(grid, max_player, min_player, max_player_turn)
           make_move(grid, min_player, x, y)

        max_player_turn = not max_player_turn
        print("Updated grid :")
        print_grid(grid)

        check_score = utility(grid, max_player, min_player)
        if check_score:
          break

        empty_loc = get_empty_locations(grid)

    score = minimax_algorithm(grid, max_player, min_player, max_player_turn)

    if score == 1:
      print("Congrats! You ('X') have won!")

    elif score == -1:
      print("You have lost! Better luck next time!")

    else:
      print("It's a draw!")