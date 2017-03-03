# -*- coding: utf-8 -*-
import pprint


def _apply_tore(x, y, game_data):
    board_x = game_data['const']['board_size']['x']
    board_y = game_data['const']['board_size']['y']
    print 'test', board_x, board_y

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
    """Move the ship of a player to an antoher position
    Parameters:
    -----------
    boat_name: name of the boat who is moving (str)
    player: The player who makes the move (int) 
    
    
    Notes:
    ------
    player: Must be one of this possibilities(0: abandoned, 1:player1, 2:player2)
    """
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


def _turn_ship(space_ship, direction_str, game_data, player):
    """Change the orientation of a ship
    Parameters:
    ------------
    space_ship: The name of the ship (str)
    direction: Must be right(Anti-clockwise) or left(clockwise) (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    # 0=up,1=up-right,2=right,3=down-right,4=down;5=down-left,6=left,7=up-left
    # Get the current direction
    position = game_data['ships'][player][space_ship]
    direction = game_data['board'][position][player][space_ship]['orientation']

    if direction_str == 'right':  # Anti-clockwise
        direction -= 1
    elif direction_str == 'left':  # clockwise
        direction += 1

    # Update the information
    game_data['board'][position][player][space_ship]['orientation'] = direction % 8  # congruency in Z
    print 'direction : ', direction % 8


def _ship_acceleration(space_ship, way, game_data, player):
    """Change the acceleration of a ship
    Parameters:
    ------------
    space_ship: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    # Get the current speed
    position = game_data['ships'][player][space_ship]
    speed = game_data['board'][position][player][space_ship]['speed']
    max_speed = _ship_characteristics(game_data['board'][position][player][space_ship]['type'])
    max_speed = max_speed['max_speed']

    # faster
    if way == 'faster':
        if speed < max_speed:
            speed += 1
    # slower
    if way == 'slower':
        if speed > 0:
            speed -= 1
    # update
    game_data['board'][position][player][space_ship]['speed'] = speed


def _ship_characteristics(ship_type):
    if ship_type == 'battlecruiser':
        return {'max_speed': 1, 'health': 20, 'attack': 4, 'range': 10, 'cost': 30}
    elif ship_type == 'destroyer':
        return {'max_speed': 2, 'health': 8, 'attack': 2, 'range': 7, 'cost': 20}
    elif ship_type == 'fighter':
        return {'max_speed': 5, 'health': 3, 'attack': 1, 'range': 5, 'cost': 10}
    else:
        print 'error'

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
    ship_position = game_data[ships][player][ship_name]

    #deals with the possible attack
    if is_in_range(ship_position, attack_position):
        #get the type of the ship attacking
        ship_type = game_data['board'][ship_position][player][ship_name][type]
        #get the information about the ship attacking
        information = _ship_characteristics(ship_type)
        #add the information of the possible attack
        attack_list += information['attack']
        attack_list += attack position
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
    for attack in atacks_list:
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

def _make_action(dictionnary, answer_one, answer_two):
    """
    Parameters:
    -----------
    dictionnary: dictionnary which contain the informations of the game
    answer_one: The command of the player one (str)
    answer_two: The command of the player two (str)
    """
    
    command = answer_one.split(' ')
    for elements in command: #split all the str in command
        action = elements.split(':') #split each command in two elements
        if action[1] == 'slower':
            _ship_acceleration(action[0],'slower', dictionnary, 1)
        elif action[1] == 'faster':
            _ship_acceleration(action[0],'faster', dictionnary, 1)
        elif action[1] == 'right':
            _turn_ship(action[0], 'right', dictionnary, 1)
        elif action[1] == 'left':
            _turn_ship(action[0], 'left', dictionnary, 1):
        elif '-' in action[2]:
            #TODO
            coordstr = action[2].split('-')
            x = coordstr[0]
            y = coordstr[1]
            
            
    command = answer_one.split(' ')
    for elements in command: #split all the str in command
        action = elements.split(':') #split each command in two elements
        if action[1] == 'slower':
            _ship_acceleration(action[0],'slower', dictionnary, 2)
        elif action[1] == 'faster':
            _ship_acceleration(action[0],'faster', dictionnary, 2)
        elif action[1] == 'right':
            _turn_ship(action[0], 'right', dictionnary,2)
        elif action[1] == 'left':
            _turn_ship(action[0], 'left', dictionnary, 2):
        elif '-' in action[2]:
            #TODO          
        

    ###TEST ZONE###


game_data = {'board': {}, 'ships': {0: {}, 1: {}, 2: {}}, 'const': {'board_size': {'x': 0, 'y': 0}}}
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)
pprint.pprint(game_data['board'])
game_data['board'][(10, 2)][0]['hugo']['speed'] = 5
_move_ship('hugo', 0, game_data)
