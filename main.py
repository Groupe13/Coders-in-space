# -*- coding: utf-8 -*-
import math
import pprint
import random


def process_order(game_data, player, player_orders, attacks):
    orders = player_orders.split(' ')
    for elements in orders:  # split all the str in orders
        action = elements.split(':')  # split each orders in two elements
        print 'TEST', action
        if action[1] == 'slower' or action[1] == 'faster':
            _ship_acceleration(action[0], action[1], game_data, player)
        elif action[1] == 'right' or action[1] == 'left':
            _turn_ship(action[0], action[1], game_data, player)
        elif '-' in action[1]:
            coord_str = action[1].split('-')
            target = (int(coord_str[0]), int(coord_str[1]))
            _check_and_memory_attack(action[0], player, target,
                                     attacks, game_data)


def _check_and_memory_attack(ship_name, player, attack_position, attacks_list, game_data):
    """Append to a list the attack if it can be made

    Parameters:
    -----------
    boat_name: name of the boat that has to attack (str)
    player: number of the player who is playing (int)
    position_attack: place where the boat has to attack (tuple)


    Note:
    -----
    If the attack cannot be made, the list is empty
    The first element is the power of the attack, the second one is the position
    """
    # get the position of the ship attacking
    ship_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][ship_position][player][ship_name]['type']
    if _is_in_range(attack_position, ship_name, player, game_data):
        # get the type of the ship attacking
        # get the information about the ship attacking
        attacks_list.append(
            {'target': attack_position,
             'power': game_data['boat_characteristics'][ship_type]['attack']})


def _make_actions(game_data, player1_orders, players2_orders):
    """
    Parameters:
    -----------
    game_data: game_data which contain the informations of the game
    player_orders: The orders of the player one (str)
    """
    attacks_list = list()
    process_order(game_data, 1, player1_orders, attacks_list)
    process_order(game_data, 2, players2_orders, attacks_list)
    _make_attacks(attacks_list, game_data)


def _game_loop(game_data):
    """
    """
    while len(game_data['ships'][1]) > 0 \
            and len(game_data['ships'][2]) > 0 \
            and game_data['variables']['last_damages'] < 10:

        player1_orders = raw_input('What does player one want to play?')
        player2_orders = raw_input('What does player two want to play?')
        _make_actions(game_data, player1_orders, player2_orders)  # need to implement it
        pprint.pprint(game_data['board'][(10, 10)])

    if game_data['variables']['last_damage'] == 10:
        player_money1 = 0
        player_money2 = 0
        for player in game_data['ships']:
            for ship in game_data['ships'][player]:
                boat_type = game_data['board'][game_data['ships'][player][ship]][player][ship]['type']
                if player == 1:
                    player_money1 += game_data['boat_characteristics'][boat_type]['cost']
                else:
                    player_money2 += game_data['boat_characteristics'][boat_type]['cost']

            if player_money1 > player_money2:
                return 1
            elif player_money1 > player_money2:
                return 2
            else:
                return random.randint(1, 2)  # determine the winner randomly

    elif len(game_data['ships'][1]) == 0:
        return 2
    elif len(game_data['ships'][2]) == 0:
        return 1


def _apply_tore(x_coordinate, y_coordinate, game_data):
    board_x = game_data['variables']['board_size']['x']
    board_y = game_data['variables']['board_size']['y']

    if x_coordinate > board_x:
        x_coordinate -= board_x
    if y_coordinate > board_y:
        y_coordinate -= board_y

    if x_coordinate < 1:
        x_coordinate += board_x
    if y_coordinate < 1:
        y_coordinate += board_y

    return x_coordinate, y_coordinate


def _move_ship(ship_name, player, game_data):
    position = game_data['ships'][player][ship_name]
    x_coordinate = position[0]
    y_coordinate = position[1]

    orientation = game_data['board'][position][player][ship_name]['orientation']
    speed = game_data['board'][position][player][ship_name]['speed']

    if speed == 0:
        return

    if orientation == 0:
        y_coordinate -= speed
    elif orientation == 1:
        x_coordinate += speed
        y_coordinate -= speed
    elif orientation == 2:
        x_coordinate += speed
    elif orientation == 3:
        x_coordinate += speed
        y_coordinate += speed
    elif orientation == 4:
        y_coordinate += speed
    elif orientation == 5:
        x_coordinate -= speed
        y_coordinate += speed
    elif orientation == 6:
        x_coordinate -= speed
    elif orientation == 7:
        x_coordinate -= speed
        y_coordinate -= speed

    new_position = _apply_tore(x_coordinate, y_coordinate, game_data)
    game_data['board'][new_position][player][ship_name] = game_data['board'][position][player][ship_name]
    del game_data['board'][position][player][ship_name]

    game_data['ships'][player][ship_name] = new_position


def _turn_ship(ship_name, direction_str, game_data, player):
    """Change the orientation of a ship
    Parameters:
    ------------
    ship_name: The name of the ship (str)
    direction: Must be right(Anti-clockwise) or left(clockwise) (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    # 0=up,1=up-right,2=right,3=down-right,4=down;5=down-left,6=left,7=up-left
    # Get the current direction
    position = game_data['ships'][player][ship_name]
    direction = game_data['board'][position][player][ship_name]['orientation']

    if direction_str == 'right':  # Anti-clockwise
        direction += 1
    elif direction_str == 'left':  # clockwise
        direction -= 1

    # Update the information
    game_data['board'][position][player][ship_name]['orientation'] = direction % 8  # congruency in Z


def _ship_acceleration(ship_name, way, game_data, player):
    """Change the acceleration of a ship
    Parameters:
    ------------
    ship_name: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    # Get the current speed
    position = game_data['ships'][player][ship_name]
    speed = game_data['board'][position][player][ship_name]['speed']
    max_speed = game_data['boat_characteristics'][game_data['board'][position][player][ship_name]['type']][
        'max_speed']  #

    # faster
    if way == 'faster':
        if speed < max_speed:
            speed += 1
    # slower
    if way == 'slower':
        if speed > 0:
            speed -= 1
    # update
    game_data['board'][position][player][ship_name]['speed'] = speed


def _is_in_range(target_position, ship_name, player, game_data):
    current_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][current_position][player][ship_name]['type']
    max_range = game_data['boat_characteristics'][ship_type]['range']

    manhattan_dist = math.fabs(target_position[0] - current_position[0]) + math.fabs(
        target_position[1] - current_position[1])
    return manhattan_dist <= max_range


def _make_attacks(attacks_list, game_data):
    """makes the attacks that can be made

    Parameters:
    -----------
    attack_list: list of the attacks that can be made (list)

    Notes:
    ------
    the list has to be made by "_check_and_memory_attack"
    """
    # get the information needed

    for attack in attacks_list:
        damage = attack['power']
        position = attack['target']

        for player in game_data['board'][position].copy():
            for ship in game_data['board'][position][player].copy():
                # attack only player's ship
                if player != 0:
                    health = game_data['board'][position][player][ship]['health'] - damage
                    if health <= 0:  # verify if the ship his destroyed
                        # delete the ship from the game
                        del game_data['board'][position][player][ship]
                        del game_data['ships'][player][ship]
                    else:
                        game_data['board'][position][player][ship]['health'] = health


def _build_board(game_board, x_size, y_size):
    """Build an empty game board.

    Parameters:
    ------------
    game_board: empty dict that will contain all the element board (dict)
    size: size of the board (x, y size must be the same ????) (tuple (int, int))
    """
    for x_coordinate in range(1, x_size + 1):
        for y_coordinate in range(1, y_size + 1):
            game_board[(x_coordinate, y_coordinate)] = {0: {}, 1: {}, 2: {}}


def _add_ship(player, ship_name, ship_type, game_data, position=(1, 1)):
    """Add a ship to a certain position.

    Parameters:
    -----------
    player: is the player's number (0: abandoned, 1:player1, 2:player2) (int)
    position: position for the new spaceship (tuple(int, int))
    ship_info: ship info (see data structure ???) (dict)
    game_board: contains all the game board element (dict)
    """
    orientation = 1
    if player == 1:
        position = game_data['variables']['default_position'][1]
    if player == 2:
        position = game_data['variables']['default_position'][2]
        orientation = 5

    game_data['board'][position][player][ship_name] = {'type': ship_type, 'orientation': orientation,
                                                       'health': game_data['boat_characteristics'][ship_type]['health'],
                                                       'speed': 0}
    game_data['ships'][player][ship_name] = position


def _build_from_cis(path, game_data):
    """Build game board from .cis file

    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: game board (dict)
    """

    file_handle = open(path, 'r')

    lines_list = file_handle.readlines()
    board_size = lines_list[0].split(' ')

    x_board_size = int(board_size[0])
    y_board_size = int(board_size[1])

    game_data['variables']['default_position'] = {}
    game_data['variables']['default_position'][1] = (10, 10)
    game_data['variables']['default_position'][2] = (x_board_size - 10, y_board_size - 10)

    _build_board(game_data['board'], x_board_size, y_board_size)
    game_data['variables']['board_size']['x'] = x_board_size
    game_data['variables']['board_size']['y'] = y_board_size
    for line in lines_list[1:]:
        line_elements = line.split(' ')  # split the line to get each element
        ship_name_type = line_elements[2].split(':')  # split to get the ship name and type

        _add_ship(0,
                  ship_name_type[0],
                  ship_name_type[1],
                  game_data,
                  (int(line_elements[0]),
                   int(line_elements[1])))  # cast str to int to get the coordonates

    ###TEST ZONE###
    ###TEST ZONE###


game_datas = {'board': {},
             'boat_characteristics': {'battlecruiser': {'attack': 4,
                                                        'cost': 30,
                                                        'health': 20,
                                                        'max_speed': 1,
                                                        'range': 10},
                                      'destroyer': {'attack': 2,
                                                    'cost': 20,
                                                    'health': 8,
                                                    'max_speed': 2,
                                                    'range': 7},
                                      'fighter': {'attack': 1,
                                                  'cost': 10,
                                                  'health': 3,
                                                  'max_speed': 5,
                                                  'range': 5}},
             'ships': {0: {}, 1: {}, 2: {}},
             'variables': {'board_size': {'x': 0, 'y': 0}, 'last_damages': 0}}

_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_datas)

names = (
'Serenity', 'Orion', 'Windsong', 'Escape', 'Whisper', 'CarpeDiem', 'SummerWind', 'Serendipity', 'Falcon', 'Falcon1',
'Falcon2')
ship_types = ('destroyer', 'battlecruiser', 'fighter')

for name in names:
    t = random.randint(0, 2)
    team = random.randint(1, 2)
    _add_ship(team, name, ship_types[t], game_datas)

pprint.pprint(game_datas['ships'])

_game_loop(game_datas)