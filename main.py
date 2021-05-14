#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile, ImageFile
from logic import player_won, comp_optimum, comp_defence, comp_attack
from copy import deepcopy

# Ev3 devices
ev3 = EV3Brick()
vertical_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
horizontal_motor = Motor(Port.A)
blocks_dispenser = Motor(Port.B, Direction.COUNTERCLOCKWISE)
block_scanner = ColorSensor(Port.S4)
touch_sensor = TouchSensor(Port.S3)

y_movement_value = 110
x_movement_value = 85

#code
def drop_brick(board):
    """
        board is [ [0 0 0] [1 0 0] [0 0 0]]  so board[1][0] = 1
        dropper always starts from board[1][2]
    """
    comp_won, x, y = comp_attack(board)
    if comp_won == False:
        comp_def, x, y = comp_defence(board)
        if comp_def == False:
            x, y = comp_optimum(board)

    board[x][y] = 2

    horizontal_motor.run_target(200, (2-y) * x_movement_value, Stop.HOLD, True)
    vertical_motor.run_angle(200, (2-x) * y_movement_value, Stop.HOLD, True)
    vertical_motor.run_angle(200, -y_movement_value/3, Stop.HOLD, True)
    blocks_dispenser.run_until_stalled(1500, Stop.COAST, None)
    blocks_dispenser.run_angle(1500, -180, Stop.HOLD, True)

    vertical_motor.run_angle(200, y_movement_value/3, Stop.HOLD, True)
    horizontal_motor.run_target(200, 5 * x_movement_value, Stop.HOLD, False)
    vertical_motor.run_angle(200, (2-x) * -y_movement_value, Stop.HOLD, False)

    if comp_won:
        ev3.speaker.say("You lost, Well Played")
        quit()
    
    for i in range(len(board)):
        print(board[i])
    return board

def scan(black_value, white_value):
    brick_color = (block_scanner.reflection() - black_value)/white_value * 100
    if brick_color < 40: return 1
    else: return 0

def column_scan(board, x, black_value, white_value):
    board[2][x] = scan(black_value, white_value)

    vertical_motor.run_angle(200, y_movement_value, Stop.HOLD, True)
    board[1][x] = scan(black_value, white_value)

    vertical_motor.run_angle(200, y_movement_value, Stop.HOLD, True)
    board[0][x] = scan(black_value, white_value)

    vertical_motor.run_angle(200, 2  * -y_movement_value, Stop.HOLD, True)
    horizontal_motor.run_angle(200, x_movement_value, Stop.HOLD, True)

    return board

def main():
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    black_value = block_scanner.reflection()
    vertical_motor.run_angle(200, y_movement_value, Stop.HOLD, True)
    white_value = block_scanner.reflection()
    vertical_motor.run_angle(200, -1.1 * y_movement_value, Stop.HOLD, True)
    horizontal_motor.run_target(200, 5 * x_movement_value, Stop.HOLD, True)

    player_moves = 0
    while True:
        if touch_sensor.pressed():
            horizontal_motor.run_target(200, 1 * x_movement_value, Stop.HOLD, True)
            board_ = deepcopy(board)
            board = column_scan(board, 2, black_value, white_value)
            board = column_scan(board, 1, black_value, white_value)
            board = column_scan(board, 0, black_value, white_value)
            horizontal_motor.run_target(200, x_movement_value, Stop.HOLD, True)

            player_moves += 1

            for i in board:
                print(i)
            print()

            if player_won(board, 1):
                ev3.speaker.say("You win, Well Played")
                quit()
                
            if player_moves == 5:
                ev3.speaker.say("It's a draw, Well Played")
                quit()

            for i in range(len(board_)):
                for j in range(len(board_)):
                    if board_[i][j] == 2: board[i][j] = 2

            board = drop_brick(board)
            horizontal_motor.run_target(200, 5 * x_movement_value, Stop.HOLD, False)
                    
                    

main()