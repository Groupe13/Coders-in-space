# -*- coding: utf-8 -*-
import math
import pprint
import random


def _update_ui(game_data):
    x_size = game_data['variables']['board_size']['x']
    y_size = game_data['variables']['board_size']['y']

    border = (150 - x_size) / 2
    border_str = ' ' * border
    x_numbers_str = border_str + '   '

    positions_save = {}

    for number in range(1, x_size+1):
        x_numbers_str += ' \033[4m%02d\033[0m' % (number)


    for player in game_data['ships']:
        for ship in game_data['ships'][player]:
            pos = game_data['ships'][player][ship]
            if not pos in positions_save:
                positions_save[pos] = 0
            positions_save[pos]+=1
    print positions_save
    print x_numbers_str

    for row in range(1, y_size + 1):
        line = border_str + ' %02d|' % row

        for column in range(1, x_size+1):
            if (column, row) in positions_save:
                line +=  '\033[4m%02d\033[0m|' % positions_save[(column, row)]
            else:
                line += '__|'

        print line
        line = ''


    print positions_save



def process_order(player, player_orders, attaks_list, game_data):
    """Procces an order asked by a player.
    
    Parameters:
    -----------
    player: number of the player who is playing (int)
    player_orders: The order wich the player want to process (str)
    attacks_list: A list wich contains all the attacks (list)
    game_data: The board and all the informations of the game (dict)
    """
    
    orders = player_orders.split(' ')
    for elements in orders:  # split all the str in orders
        action = elements.split(':')  # split each orders in two elements
        print 'TEST', action
        if action[1] == 'slower' or action[1] == 'faster':
            _ship_acceleration(player, action[0], action[1], game_data)
        elif action[1] == 'right' or action[1] == 'left':
            _turn_ship(player, action[0], action[1], game_data)
        elif '-' in action[1]:
            coord_str = action[1].split('-')
            target = (int(coord_str[0]), int(coord_str[1]))
            _check_and_memory_attack(player, action[0], target,
                                     attaks_list, game_data)


def _check_and_memory_attack(player, ship_name, attack_position, attacks_list, game_data):
    """Append to a list the attack if it can be made.
   
    Parameters:
    -----------
    player: number of the player who is playing (int)
    ship_name: name of the boat that has to attack (str)
    attack_position: place where the boat has to attack (tuple)
    attacks_list: A list wich contains all the attacks (list)
    game_data: The board and all the informations of the game (dict)
    
    Note:
    -----
    If the attack cannot be made, the list is empty
    The first element is the power of the attack, the second one is the position
   """
    # get the position of the ship attacking
    ship_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][ship_position][player][ship_name]['type']
    if _is_in_range(player, ship_name, attack_position, game_data):
        # get the type of the ship attacking
        # get the information about the ship attacking
        attacks_list.append(
            {'target': attack_position,
             'power': game_data['boat_characteristics'][ship_type]['attack']})


def _make_actions(player1_orders, player2_orders, game_data):
    """Prepare the orders for process_order and process.
   
    Parameters:
    -----------
    player1_orders: The orders of the player one (str)
    player2_orders: The orders of the player two (str)
    game_data: The board and all the informations of the game (dict)
    """
   
    attacks_list = list()
    process_order(1, player1_orders, attacks_list, game_data)
    process_order(2, player2_orders, attacks_list, game_data)

    _make_attacks(attacks_list, game_data)

def _move_all_ships(game_data):
    """"""
    for player in game_data['ships']:
        if player != 0:
            for ship_name in game_datas['ships'][player]:
                _move_ship(player, ship_name, game_data)

def _game_loop(game_data):
    """The main function wich choose a winner and execute the game.
    
    Parameters:
    -----------
    game_data: The board and all the informations of the game (dict)
    """

    while len(game_data['ships'][1]) > 0 \
            and len(game_data['ships'][2]) > 0 \
            and game_data['variables']['last_damages'] < 10:

        player1_orders = raw_input('Player1 - What do you want to play ? : ').lower()
        player2_orders = raw_input('Player2 - What do you want to play ? : ').lower()
        _make_actions(player1_orders, player2_orders, game_data)  # need to implement it
        _move_all_ships(game_data)


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
    """Apply the effect of a tore if the ship is outside the board.
    
    Parameters:
    -----------
    x_coordinate: The abscissa of the ship (int)
    y_coordinate: The ordinate of the sip (int) 
    game_data: The board and all the informations of the game (dict)
    """
 
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


def _move_ship(player, ship_name, game_data):
    """Move the ship of a player to a new position.
    
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    game_data: The board and all the informations of the game (dict)
    """
   
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


def _turn_ship(player, ship_name, direction_str, game_data):
    """Change the orientation of a ship.
   
    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    direction_str: Must be left(Anti-clockwise) or right(clockwise) (str)
    game_data: The board and all the informations of the game (dict)
    """
    
    # 0=up,1=up-right,2=right,3=down-right,4=down;5=down-left,6=left,7=up-left
    # Get the current direction
    position = game_data['ships'][player][ship_name]
    direction = game_data['board'][position][player][ship_name]['orientation']

    if direction_str == 'right':  # clockwise
        direction += 1
    elif direction_str == 'left':  #  Anti-clockwise
        direction -= 1

    # Update the information
    game_data['board'][position][player][ship_name]['orientation'] = direction % 8  # congruency in Z


def _ship_acceleration(player, ship_name, way, game_data):
    """Change the acceleration of a ship.
    
    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: The board and all the informations of the game (dict)
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


def _is_in_range(player, ship_name, target_position, game_data):
    """Verify if the case attacked by a ship is in the range of or not.
    
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    target_position: The target of the ship (tuple)
    game_data: The board and all the informations of the game (dict)
        
    Returns:
    --------    
    in_range: if the place can be attacked or not (bool)
    
    Notes:
    ------
    in_range is True if the case can be attacked, False otherwhise
    """
    
    current_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][current_position][player][ship_name]['type']
    max_range = game_data['boat_characteristics'][ship_type]['range']

    manhattan_dist = math.fabs(target_position[0] - current_position[0]) + math.fabs(
        target_position[1] - current_position[1])
    return manhattan_dist <= max_range


def _make_attacks(attacks_list, game_data):
    """makes the attacks that can be made.
   
    Parameters:
    -----------
    attacks_list: list of the attacks that can be made (list)
    
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


def _build_board(x_size, y_size, game_board):
    """Build an empty game board.
    
    Parameters:
    ------------
    x_size: The size of the board in abscissa (int)
    y_size: The ziez of the board in ordinate (int)
    game_board: empty dict that will contain all the element of board (dict)
    """
    
    for x_coordinate in range(1, x_size + 1):
        for y_coordinate in range(1, y_size + 1):
            game_board[(x_coordinate, y_coordinate)] = {0: {}, 1: {}, 2: {}}


def _buy_ships(game_data):
    """Ask to the player what he wants to buy.
   
    Parameters:
    ------------
    game_board: empty dict that will contain all the element of board (dict)
    """
    
    player1_orders = raw_input('Player1 - What boat do you want to buy ? :').lower()
    player2_orders = raw_input('Player2 - What boat do you want to buy ? :').lower()

    ship_list_player1 = player1_orders.split(' ')
    ship_list_player2 = player2_orders.split(' ')
    _buy_and_add_ships(1, ship_list_player1, game_data)
    _buy_and_add_ships(2, ship_list_player2, game_data)


def _buy_and_add_ships(player, ships_list, game_data):
    """Place the new ship one the board.
    
    Parameters:
    ------------
    player: The player who makes the action (int)
    ships_list: The list wich contains all the new ships (list)
    game_board: empty dict that will contain all the element of board (dict)
    """
    wallet = 100

    for ship in ships_list:
        name, ship_type = ship.split(':')
        wallet -= game_data['boat_characteristics'][ship_type]['cost']
        if wallet >= 0:
            _add_ship(player, name, ship_type, game_data)

    game_data['variables']['wallet'][player] = 0




def _add_ship(player, ship_name, ship_type, game_data, position=(1, 1)):
    """Add a ship to a certain position.
   
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    ship_type: The type of the boat (str)
    position: position for the new spaceship (tuple(int, int))
    game_data: The board and all the informations of the game (dict)
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
    print 'ships added!'


def _build_from_cis(path, game_data):
    """Build game board from .cis file.
    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: The board and all the informations of the game (dict)
    """

    file_handle = open(path, 'r')

    lines_list = file_handle.readlines()
    board_size = lines_list[0].split(' ')

    x_board_size = int(board_size[0])
    y_board_size = int(board_size[1])

    game_data['variables']['default_position'] = {}
    game_data['variables']['default_position'][1] = (10, 10)
    game_data['variables']['default_position'][2] = (x_board_size - 10, y_board_size - 10)

    _build_board(x_board_size, y_board_size, game_data['board'])
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
def _buy_IA():
    wallet = 100
    action =''
    name = i
    while wallet > 0:
        action += name
        ship = random.randint(1,3)
        if ship == 1:
            action += 'fighter'
            wallet -= 10
        elif ship ==2:
            action += 'destroyer'
            wallet -= 20
        else:
            action += 'battlecruiser'
            wallet -= 30
        name += 'a'
    return action

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
             'variables': {'board_size': {'x': 0, 'y': 0}, 'last_damages': 0, 'wallet':{1:100, 2:100}}}

_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_datas)

names = (
'Serenity', 'Orion', 'Windsong', 'Escape', 'Whisper', 'CarpeDiem', 'SummerWind', 'Serendipity', 'Falcon', 'Falcon1',
'Falcon2')
ship_types = ('destroyer', 'battlecruiser', 'fighter')

for name in names:
    t = random.randint(0, 2)
    team = random.randint(1, 2)
    _add_ship(0, name, ship_types[t], game_datas, (random.randint(1, 30), random.randint(1, 30)))
_update_ui(game_datas)

pprint.pprint(game_datas['ships'])
