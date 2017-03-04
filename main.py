# -*- coding: utf-8 -*-
import pprint
import random

def _make_actions():
    """"""

def _game_loop(game_data):
    """
    """
    while len(game_data['ships'][1]) > 0 and len(game_data['ships'][2]) > 0 and game_data['variables']['last_damage'] < 10: # <= ????
        answer_one = raw_input('What does player one want to play?')
        answer_two = raw_input('What does player two want to play?')
        #_make_actions(game_data, answer_one, answer_two) # need to implement it

    if game_data['variables']['last_damage'] == 10:
        player_money1 = 0
        player_money2 = 0
        for player in game_data['ships']:
            for ship in game_data['ships'][player]:
                print player, ship
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
                winner = random.randint(1, 2)
                return winner

    elif len(game_data['ships'][1])==0:
        return 2
    elif len(game_data['ships'][2])==0:
        return 1

def _apply_tore(x, y, game_data):
    board_x = game_data['variables']['board_size']['x']
    board_y = game_data['variables']['board_size']['y']

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

    if speed == 0:
        return

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
    print 'direction : ', direction % 8


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
    max_speed = game_data['boat_characteristics'][game_data['board'][position][player][ship_name]['type']]['max_speed'] #

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

def _check_and_memory_attack(ship_name, player, attack_position):
    """Returns a list of the attack if it can be made

    Parameters:
    -----------
    boat_name: name of the boat that has to attack (str)
    player: number of the player who is playing (int)
    position_attack: place where the boat has to attack (tuple)

    Return:
    -------
    attack_list: list of the attack if it can be made (list)

    Note:
    -----
    If the attack cannot be made, the list is empty
    The first element is the power of the attack, the second one is the position
    """
    #variable declaration
    attack_list = ()
    #get the position of the ship attacking
    ship_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][ship_position][player][ship_name]['type']
    if _is_in_range(attack_position, ship_name, player, game_data):
        #get the type of the ship attacking
        #get the information about the ship attacking
        information = game_data['boat_characteristics'][ship_type]
        #add the information of the possible attack
        attack_list += information['attack']
        attack_list += attack_position
    return attack_list


def _make_attacks (attacks_list):

    """makes the attacks that can be made

    Parameters:
    -----------
    attack_list: list of the attacks that can be made (list)

    Notes:
    ------
    the list has to be made by "_check_and_memory_attack"
    """
    #get the information needed
    for attack in attacks_list:
        damage = attack[0]
        position = attack[1]

        for player in game_data['board'][position]:
            for ship in player:
                #attack only player's ship
                if player == 1 or player == 2:
                    ship['health'] -= damage  # apply damages
                    if ship['health'] <= 0:  # verify if the ship his destroyed
                        # delete the ship from the game
                        del game_data['board'][position][player][ship]
                        del game_data['ships'][player][ship]


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


def _add_ship(player, ship_name, ship_type, game_data, position = (1,1) ):
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

    game_data['board'][position][player][ship_name] = {'type': ship_type, 'orientation': orientation, 'health': game_data['boat_characteristics'][ship_type]['health'], 'speed': 0}
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

    game_data['variables']['default_position'] = {}
    game_data['variables']['default_position'][1] = (10,10)
    game_data['variables']['default_position'][2] = (x_board_size - 10, y_board_size - 10)


    print game_data['variables']['default_position'][1], game_data['variables']['default_position'][2]

    _build_board(game_data['board'], x_board_size, y_board_size)
    game_data['variables']['board_size']['x'] = x_board_size
    game_data['variables']['board_size']['y'] = y_board_size
    for line in lines_list[1:]:
        line_elements = line.split(' ')  # split the line to get each element
        ship_name_type = line_elements[2].split(':')  # split to get the ship name and type

        _add_ship(0, ship_name_type[0], ship_name_type[1],
                  game_data, (int(line_elements[0]), int(line_elements[1])))  # cast str to int to get the coordonates


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
    ###TEST ZONE###




game_data = {'board': {},
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

pprint.pprint(game_data)
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)
_add_ship(1, 'hugo', 'fighter', game_data)
#pprint.pprint(game_data['board'])
_ship_acceleration('hugo', 'faster', game_data, 1)
_move_ship('hugo', 1, game_data)
#pprint.pprint(game_data['board'])

game_data['variables']['last_damage'] = 10
print _game_loop(game_data)
