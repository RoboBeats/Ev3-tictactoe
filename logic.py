from copy import deepcopy

def player_won(board, occupant):
    for i in range(len(board)):
        if board[i] == [occupant, occupant, occupant]:
            return True

    diagonal_win = 0
    diagonal_win2 = 0
    for i in range(len(board)):
        if board[i][i] == occupant:
            diagonal_win += 1
        if board[i][2-i] == occupant:
            diagonal_win2 += 1
    if diagonal_win == 3 or diagonal_win2 == 3:
        return True

    for i in range(len(board)):
        win = 0
        for j in range(len(board)):
            if board[j][i] == occupant:
                win += 1
        if win == 3:
            return True
    return False
def comp_defence(inp_board):
    for i in range(len(inp_board)):
        for j in range(len(inp_board)):
            if inp_board[i][j] == 0:
                board_ = deepcopy(inp_board)
                board_[i][j] = 1
                if player_won(board_, 1):
                    board_[i][j] = 2
                    return True, i, j
    return False, 0, 0
def comp_attack(inp_board):
    for i in range(len(inp_board)):
        for j in range(len(inp_board)):
            if inp_board[i][j] == 0:
                board_ = deepcopy(inp_board)
                board_[i][j] = 2
                if player_won(board_, 2):
                    return True, i, j
    return False, 0, 0
def comp_optimum(inp_board):
    if  inp_board == [[1, 0, 0], [0, 2, 0], [0, 0, 1]] or inp_board == [[0, 0, 1], [0, 2, 0], [1, 0, 0]]:
             return 0, 1
    if inp_board == [[2, 0, 0], [0, 1, 0], [0, 0, 1]]:
        return 0, 2

    possible_wins = 0
    possible_wins_ = 0
    row_ = 0
    column_ = 0
    row = 0
    column = 0
    for i in range(len(inp_board)):
        for j in range(len(inp_board)):
            board_ = deepcopy(inp_board)
            if inp_board[i][j] == 0:
                board_[i][j] = 2
                possible_wins_, row_, column_ = possible_win(board_, i, j, possible_wins)
                if possible_wins < possible_wins_:
                    possible_wins = deepcopy(possible_wins_)
                    row = deepcopy(row_)
                    column = deepcopy(column_)
    inp_board[row][column] = 2
    return row, column
def possible_win(board, row, column, max_possible_win):
    possible_wins = 0
    win_row = 0
    for i in range(len(board)):
        if board[i][column] == 2 or board[row][i] == 0:
            win_row += 1
    if win_row == 3:
        possible_wins += 1
    win_column = 0
    for i in range(len(board)):
        if board[row][i] == 2 or board[row][i] == 0:
            win_column += 1
    if win_column == 3:
        possible_wins += 1
    diagonal_win = 0
    diagonal_win2 = 0
    for i in range(len(board)):
        if board[i][i] == 0 or board[i][i] == 2:
            diagonal_win += 1
        if board[i][2-i] == 0 or board[i][2-i] == 2:
            diagonal_win2 += 1
    if diagonal_win == 3:
        possible_wins += 1
    if diagonal_win2 == 3:
        possible_wins += 1
    if possible_wins > max_possible_win:
        return possible_wins, row, column
    else:
        return max_possible_win, row, column
