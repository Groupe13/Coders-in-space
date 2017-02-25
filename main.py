# -*- coding: utf-8 -*-
import os
import math
import pprint


def _apply_tore(x, y, game_data):
    """"""
    board_x = game_data['const']['board_size']['x']
    board_y = game_data['const']['board_size']['y']
    print 'test', board_x,board_y

    if x > board_x:
        x -= board_x
    if y > board_y:
        y -= board_y

    if x < 1:
        x += board_x
    if y < 1:
        y += board_y

    return (x, y)



def _move_ship(ship_name, player, game_data):

    position = game_data['ships'][player][ship_name]
    print position
    x = position[0]
    y = position[1]

    orientation = game_data['board'][position][player][ship_name]['orientation']
    speed = game_data['board'][position][player][ship_name]['speed']

    if orientation == 0:
        y -= speed
    elif orientation == 1:
        x += speed
        y -= speed
    elif orientation == 2:
        x += speed
    elif orientation == 3:
        x += speed
        y += speed
    elif orientation == 4:
        y += speed
    elif orientation == 5:
        x -= speed
        y += speed
    elif orientation == 6:
        x -= speed
    elif orientation == 7:
        x -= speed
        y -= speed


    new_position = _apply_tore(x, y, game_data)
    print 'new position : ', new_position
    game_data['board'][new_position][player][ship_name] = game_data['board'][position][player][ship_name]
    del game_data['board'][position][player][ship_name]

    game_data['ships'][player][ship_name] = new_position


def _turn_ship(space_ship,direction,game_data,player):
    """Change the orientation of a ship
    Parameters:
    ------------
    space_ship: The name of the ship (str)
    direction: Must be right(Anti-clockwise) or left(clockwise) (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    #0=up,1=up-right,2=right,3=down-right,4=down;5=down-left,6=left,7=up-left
    #Get the current direction
    position = game_data['ships'][player][space_ship]
    direction = game_data['board'][position][player][space_ship]['orientation']
    
    if direction == 'right':#Anti-clockwise
        if direction == 1:
            new_direction = 8
        else: 
            new_direction = direction - 1
    
    elif direction == 'left':#clockwise
        if direction == 8:
            new_direction = 1
        else: 
            new_direction = direction + 1
   
    #Update the information
    game_data['board'][position][player][space_ship]['orientation'] = new_direction


def _ship_acceleration(space_ship,way,game_data,player):
    """Change the acceleration of a ship
    Parameters:
    ------------
    space_ship: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    #Get the current speed
    position = game_data['ships'][player][space_ship]
    speed = game_data['board'][position][player][space_ship]['speed']
    max_speed = _ship_characteristics(game_data['board'][position][player][space_ship]['type'])
    max_speed = max_speed['max_speed']
    
    #faster
    if way == 'faster':
        if speed < max_speed:
            speed += 1
    #slower
    if way == 'slower':
        if speed > 0:
            speed -= 1
    #update
    game_data['board'][position][player][space_ship]['speed'] = speed

    """"""


def _ship_characteristics(ship_type):
    if ship_type == 'battlecruiser':
        return {'max_speed': 1, 'health': 20, 'attack': 4, 'range': 10, 'cost': 30}
    elif ship_type == 'destroyer':
        return {'max_speed': 2, 'health': 8, 'attack': 2, 'range': 7, 'cost': 20}
    elif ship_type == 'fighter':
        return {'max_speed': 5, 'health': 3, 'attack': 1, 'range': 5, 'cost': 10}
    else:
        print 'error'


def _attack_position(position, ship_info, game_board):
    damage = ship_info['damage']
    for player in game_board[position]:  # iterate through the players
        for ship in player:  # iterate through the player's ship
            ship['health'] -= damage  # apply damages
            if ship['health'] <= 0:  # verify if the ship his destroyed
                del game_board[position][player]  # delete the ship from the game


def _build_board(game_board, x, y):
    """Build an empty game board.

    Parameters:
    ------------
    game_board: empty dict that will contain all the element board (dict)
    size: size of the board (x, y size must be the same ????) (tuple (int, int))
    """
    for mx in range(1, x + 1):
        for my in range(1, y + 1):
            game_board[(mx, my)] = {0: {}, 1: {}, 2: {}}


def _add_ship(player, position, ship_name, ship_type, game_data):
    """Add a ship to a certain position.

    Parameters:
    -----------
    player: is the player's number (0: abandoned, 1:player1, 2:player2) (int)
    position: position for the new spaceship (tuple(int, int))
    ship_info: ship info (see data structure ???) (dict)
    game_board: contains all the game board element (dict)
    """
    orientation = 1
    if player == 2:
        orientation = 5

    game_data['board'][position][player][ship_name] = {'type': ship_type, 'orientation': orientation,
                                                       'health': _ship_characteristics(ship_type)['health'], 'speed': 0}
    game_data['ships'][player][ship_name] = position


def _build_from_cis(path, game_data):
    """Build game board from .cis file

    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: game board (dict)
    """

    fh = open(path, 'r')

    lines_list = fh.readlines()
    board_size = lines_list[0].split(' ')

    x_board_size = int(board_size[0])
    y_board_size = int(board_size[1])

    _build_board(game_data['board'], x_board_size, y_board_size)
    game_data['const']['board_size']['x'] = x_board_size
    game_data['const']['board_size']['y'] = y_board_size
    for line in lines_list[1:]:
        line_elements = line.split(' ')  # split the line to get each element
        ship_name_type = line_elements[2].split(':')  # split to get the ship name and type

        _add_ship(0, (int(line_elements[0]), int(line_elements[1])), ship_name_type[0], ship_name_type[1],
                  game_data)  # cast str to int to get the coordonates


def _buy_boat(player, game_data):
    """Buy the boat for a given player

    Parameters:
    ------------
    player: The player who buy a boat (int)
    game_data: The game board (dict)

    Notes:
    ---------
    player: Must be one of this possibilities(0: abandoned, 1:player1, 2:player2)
    """



    ###TEST ZONE###


game_data = {'board': {}, 'ships': {0: {}, 1: {}, 2: {}}, 'const':{'board_size':{'x':0, 'y':0}}}
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)
pprint.pprint(game_data['board'])
game_data['board'][(10, 2)][0]['hugo']['speed'] = 5
_move_ship('hugo', 0, game_data)

