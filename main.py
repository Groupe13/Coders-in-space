# -*- coding: utf-8 -*-
import time
import random
import termcolor
import socket

def main(path, player_1, player_2):
    """Execute the game

    Parameters:
    -----------
    path: path of the .cis file which contain the information of the game played (path)
    player_1: type of the player one (str)
    player_2: type of the player two (str)

    Notes:
    ------
    The types can be IA, remote or player

    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    """
    
    #initialisation of the main dictionnary
    game_data = {'board': {},
                 'ship_characteristics': {'battlecruiser': {'attack': 4,
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
                 'variables': {'board_size': {'x': 0, 'y': 0}, 'last_damages': 0, 'wallet': {1: 100, 2: 100}}}


    #building of the board
    _build_from_cis(path, game_data)
    _buy_ships(game_data, player_1, player_2)
    #initialisation of the user design
    _update_ui(game_data)
    #connect if playing with remote player
    if player_1 == 'remote' or player_2 == 'remote':
        connection = connect_to_player(player_id)
    #execution of the game
    winner = _game_loop(game_data, player_1, player_2, connection)
    print 'The winner is player %d' (winner)

def _game_loop(game_data,player1,player2, connection = None):
    """Execute the game and return the winner when the game is over.

    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)
    player1: type of player (str)
    player2: type of player (str)
    connection: sockets to receive/send orders (tuple)     
    Notes:
    ------
    Player can be IA, remote or player

    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    
    """
    #check if the game is ended
    while len(game_data['ships'][1]) > 0 \
            and len(game_data['ships'][2]) > 0 \
            and game_data['variables']['last_damages'] < 10:
        
        #turn of each type of player
        if player1 == 'IA':
            player1_orders = _get_IA_orders(game_data, 1)
        elif player1 == 'remote':
            player1_orders = get_remote_orders(connection)
        else:
            player1_orders = raw_input('Player1 - What do you want to play ? : ').lower()
        if player1 == 'IA' and player2 =='remote':
            notify_remote_orders(connection, player1_orders)
        
        if player2 == 'IA':
            player2_orders = _get_IA_orders(game_data, 2)
        elif player2 == 'remote':
            player2_orders = get_remote_orders(connection)
        else:
            player2_orders = raw_input('Player2 - What do you want to play ? : ').lower()           
        if player1 == 'remote' and player2 =='IA':
            notify_remote_orders(connection, player2_orders)    
        #update the number of turn without damages
        game_data['variables']['last_damages'] += 1
        #execute all the actions asked
        _make_actions(player1_orders, player2_orders, game_data)
        #move all the ships  
        _move_all_ships(game_data)
        #verify if abandonned ships can be caught
        _get_neutral_ships(game_data)
        #update the user design
        _update_ui(game_data)




    # deal with the end of the game
    
    #deal with the case where  turn has passed without any damage
    if game_data['variables']['last_damages'] == 10:
        
        #initialisation of the players money
        player_money1 = 0
        player_money2 = 0
        #deal with each player
        for player in game_data['ships']:
            #deal with each ship
            for ship in game_data['ships'][player]:
                #get the type of the left ship
                ship_type = game_data['board'][game_data['ships'][player][ship]][player][ship]['type']
                
                #get the price of the type of ship for each player
                if player == 1:
                    player_money1 += game_data['ship_characteristics'][ship_type]['cost']
                else:
                    player_money2 += game_data['ship_characteristics'][ship_type]['cost']
                    
            #verify who has won the game
            if player_money1 > player_money2:
                return 1
            elif player_money1 < player_money2:
                return 2
            else:
                # determine the winner randomly
                return random.randint(1, 2)  
    #deal with the case where the number of ships is under 0
    elif len(game_data['ships'][1]) == 0:
        return 2
    elif len(game_data['ships'][2]) == 0:
        return 1

#---------------------------------------------------------------------------------------------------#

def _update_ui(game_data):
    """Show the board and the information about the game played
    
    Parameters:
    -----------
    game_data: dictionary which contains all the information about the game played (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 5/03/17)
    """
    print ''
    #get board size
    x_size = game_data['variables']['board_size']['x'] 
    y_size = game_data['variables']['board_size']['y']

    # calculate baord border (to center the board)
    border = (190 -2 - x_size * 4) / 2
    border_str = ' ' * border
    x_numbers_str = border_str + '   '

    positions_save = {}  # save position that contains ships

    for number in range(1, x_size + 1):
        x_numbers_str += ' \033[4m%02d\033[0m' % (number)
    #initialisation of each player
    ships_informations = {0: '', 1: '', 2: ''}
    
    #deal with each player
    for player in game_data['ships']:
        #deal with each ship
        for ship in game_data['ships'][player]:
            #get the position of the ship
            position = game_data['ships'][player][ship]
            #get the information of the ship
            ship_info = game_data['board'][position][player][ship]
            #add the information of the ship 
            ships_informations[player] += '%s:%s:%s:h%d:o%d:s%d' % (ship, position, ship_info['type'], ship_info['health'], ship_info['orientation'], ship_info['speed']) + ' - '
            if not position in positions_save:
                positions_save[position] = 0
            positions_save[position] += 1
    # print positions_save
    print x_numbers_str

    for row in range(1, y_size + 1):
        line = border_str + ' %02d|' % row

        for column in range(1, x_size + 1):
            if (column, row) in positions_save:
                line += termcolor.colored('\033[4m%02d\033[0m|' % positions_save[(column, row)], 'cyan')
            else:
                line += '__|'

        print line
    print ''  # Empty line
    # max 9 line left
    line_left = 47 - y_size
    for p in ships_informations:
        line_size = len(ships_informations[p])
        line_left -= line_size / 190
        print 'Team %d : %s' % (p, ships_informations[p])

    print line_left

    if line_left >= 0:
        for i in range(0, line_left):
            print ''

#---------------------------------------------------------------------------------------------------#

def _process_order(player, player_orders, attacks_list, game_data):
    """Procces an order asked by a player.

    Parameters:
    -----------
    player: number of the player who is playing (int)
    player_orders: The orders that the player want to process (str)
    attacks_list: The list which will contain the possible attacks (list)
    game_data: Dictionary which contain all the information of the game (dict)

    Notes:
    ------
    player_orders must have the same syntax than the orders given by the player
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    """

    # split all the str in orders
    for elements in player_orders.split(' '): 
        # split each orders in two elements (ship and action)
        action = elements.split(':')
        # verify tat the ship exist or is owned by the player
        if not action[0] in game_data['ships'][player]:  
            print 'Error, the ship "%s" does not exist, or is not yours' % (action[0])
        else:
            #deal with each case of action
            if action[1] == 'slower' or action[1] == 'faster':
                _ship_acceleration(player, action[0], action[1], game_data)
            elif action[1] == 'right' or action[1] == 'left':
                _turn_ship(player, action[0], action[1], game_data)
            elif '-' in action[1]:
                # get position to attack
                coord_str = action[1].split('-')  
                # cast to str
                target = (int(coord_str[0]), int(coord_str[1]))  
                #get all the attacks that have to be made
                _check_and_memory_attack(player, action[0],target, attacks_list, game_data)                
            else:
                print 'The order "%s" can\'t be executed' % action[1]

#---------------------------------------------------------------------------------------------------#

def _check_and_memory_attack(player, ship_name, attack_position, attacks_list, game_data):
    """Append  the attack to a list if it can be made.
    Parameters:
    -----------
    player: number of the player who is playing (int)
    ship_name: name of the ship that has to attack (str)
    attack_position: place where the ship has to attack (tuple)
    attacks_list: A list wich contains all the attacks (list)
    game_data: Dictionary which contain all the information of the game (dict)

    Note:
    -----
    If the attack cannot be made, nothing is added to the list, otherwhise, there is a dictionnary which contain 'target' and 'power'
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hallaert Elise (V.1 5/03/17)
    """
    # get the position of the ship attacking
    ship_position = game_data['ships'][player][ship_name]
    #get the type of the ship attacking
    ship_type = game_data['board'][ship_position][player][ship_name]['type']
    #verify if the case attacked is in the range of the ship attacking
    if _is_in_range(player, ship_name, attack_position, game_data):
        # add the information of the possible attack
        attacks_list.append(
            {'target': attack_position,'power': game_data['ship_characteristics'][ship_type]['attack']})

#---------------------------------------------------------------------------------------------------#

def _make_actions(player1_orders, player2_orders, game_data):
    """Make all the possible actions asked by the players and the shifting

    Parameters:
    -----------
    player1_orders: The orders of the player one (str)
    player2_orders: The orders of the player two (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    """
    #initialisation of the future list of possible attacks
    attacks_list = list()
    if player1_orders:
        #deal with the orders of the player one
        _process_order(1, player1_orders, attacks_list, game_data)
    if player2_orders:
        #deal with the orders of the player two
        _process_order(2, player2_orders, attacks_list, game_data)
    #execute the attacks
    _make_attacks(attacks_list, game_data)

#---------------------------------------------------------------------------------------------------#

def _move_all_ships(game_data):
    """Move all the ship

    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    """
    #make the moves of the ships
    for player in game_data['ships']:
        #deal only with the ships which are not abandonned 
        if player != 0:
            for ship_name in game_data['ships'][player]:
                #move the ship
                _move_ship(player, ship_name, game_data)

#---------------------------------------------------------------------------------------------------#

def _apply_tore(x_coordinate, y_coordinate, game_data):
    """Apply the effect of a tore if the ship is outside the board.

    Parameters:
    -----------
    x_coordinate: The abscissa of the ship (int)
    y_coordinate: The ordinate of the sip (int)
    game_data: Dictionary which contain all the information of the game(dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 4/03/17)
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

#---------------------------------------------------------------------------------------------------#

def _get_neutral_ships(game_data):
    """add the abandonned ships to the team of the player
    
    Parameters:
    -----------
    game_data: dictionnary which contain all the information of the game (dict)
    
    Note:
    -----
    Only the ships which belong to a team can move
    
    Version:
    --------
    specification: Hugo Jacques (V.1 3/04/17)    
    """
    #deal with each abandonned ship
    for ship in game_data['ships'][0].copy():
        position = game_data['ships'][0][ship]
        player = None

        #treat the cases where the ship can be captured
        if game_data['board'][position][1] and not game_data['board'][position][2]:
            player = 1
        elif not game_data['board'][position][1] and game_data['board'][position][2]:
            player = 2
        
        #treat the case where the ship is captured
        if player != None:
            if ship in game_data['board'][position][player][ship]:
                new_ship = ship+'_2'
            game_data['board'][position][player][ship] = game_data['board'][position][0][new_ship]
            game_data['ships'][player][ship] = game_data['ships'][0][new_ship]
            
            del game_data['board'][position][0][ship]
            del game_data['ships'][0][ship]

#---------------------------------------------------------------------------------------------------#

def _move_ship(player, ship_name, game_data):
    """Move the ship of a player to a new position.

    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Note:
    -----
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)

    """

    #get the position of the ship
    position = game_data['ships'][player][ship_name]
    #get the coordinates of the ship
    x_coordinate = position[0]
    y_coordinate = position[1]
    
    #get th eorientation of the ship
    orientation = game_data['board'][position][player][ship_name]['orientation']
    #get the speed of the ship
    speed = game_data['board'][position][player][ship_name]['speed']

    #change the position of the ship depending to the speed and the orientation 
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
    
    #part to modify?
    new_position = _apply_tore(x_coordinate, y_coordinate, game_data)
    #change the position of the ship
    game_data['board'][new_position][player][ship_name] = game_data['board'][position][player][ship_name]
    

    #change the position of the ship     
    game_data['ships'][player][ship_name] = new_position

#---------------------------------------------------------------------------------------------------#

def _turn_ship(player, ship_name, direction_str, game_data):
    """Change the orientation of a ship.

    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    direction_str: Must be left(Anti-clockwise) or right(clockwise) (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Note:
    -----
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)
    """

    # 0=up,1=up-right,2=right,3=down-right,4=down;5=down-left,6=left,7=up-left
    # Get the current direction
    position = game_data['ships'][player][ship_name]
    direction = game_data['board'][position][player][ship_name]['orientation']

    if direction_str == 'right':  # clockwise
        direction += 1
    elif direction_str == 'left':  # Anti-clockwise
        direction -= 1

    # Update the information
    game_data['board'][position][player][ship_name]['orientation'] = direction % 8  # congruency in Z

#---------------------------------------------------------------------------------------------------#

def _ship_acceleration(player, ship_name, way, game_data):
    """Change the speed of a ship.

    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Note:
    -----
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hugo Jacques (V.1 4/03/17)
    """

    # Get the current speed and position
    position = game_data['ships'][player][ship_name]
    speed = game_data['board'][position][player][ship_name]['speed']
    #get the max speed of the ship
    max_speed = game_data['ship_characteristics'][game_data['board'][position][player][ship_name]['type']]['max_speed']

    # faster
    if way == 'faster' and speed < max_speed:
        # update the speed of the ship
        game_data['board'][position][player][ship_name]['speed'] += 1
    # slower
    if way == 'slower' and speed > 0:
        # update the speed of the ship
        game_data['board'][position][player][ship_name]['speed'] -= 1

#---------------------------------------------------------------------------------------------------#

def _is_in_range(player, ship_name, target_position, game_data):
    """Verify if the case attacked by a ship is in the range or not.

    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    target_position: The target of the ship (tuple)
    game_data: Dictionary which contain all the information of the game (dict)

    Returns:
    --------
    in_range: if the place can be attacked or not (bool)

    Notes:
    ------
    in_range is True if the case can be attacked, False otherwhise
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Métens Guillaume (V.1 5/03/17)
    """
    #get the current position
    current_position = game_data['ships'][player][ship_name]
    #get the type of the ship
    ship_type = game_data['board'][current_position][player][ship_name]['type']
    #get the range of the ship
    max_range = game_data['ship_characteristics'][ship_type]['range']

    #Check if we need to apply "tore" effect
    #Calculate the tore_value:
    
    #Tore_value_x
    if (game_data['variables']['board_size']['x']//2) < (game_data['variables']['board_size']['x']/2.0):
        tore_value_x = (game_data['variables']['board_size']['x']//2) +1
    else:
        tore_value_x = (game_data['variables']['board_size']['x']/2)
    
    #Tore_value_y
    if (game_data['variables']['board_size']['y']//2) < (game_data['variables']['board_size']['y']/2.0):
        tore_value_y = (game_data['variables']['board_size']['y']//2) +1
    else:
        tore_value_y = (game_data['variables']['board_size']['y'])/2
    
    # 4 cases => 4 manhattan_dist
    #Tore need to be apply in x AND Y
    if abs(target_position[0] - current_position[0]) >= tore_value_x and abs(target_position[1] - current_position[1]) >= tore_value_y:
        manhattan_dist = (game_data['variables']['board_size']['x'] - abs(target_position[0] - current_position[0]) ) + ( 
        game_data['variables']['board_size']['y'] - abs(target_position[1] - current_position[1]))
    
    #Tore need to be apply in X
    elif abs(target_position[0] - current_position[0]) >= tore_value_x and abs(target_position[1] - current_position[1]) < tore_value_y:
        manhattan_dist = (game_data['variables']['board_size']['x'] - abs(target_position[0] - current_position[0]) ) + abs(target_position[1] - current_position[1])
   
    #Tore need to be apply in Y
    elif abs(target_position[0] - current_position[0]) < tore_value_x and abs(target_position[1] - current_position[1]) >= tore_value_y:
        manhattan_dist = abs(target_position[0] - current_position[0]) + (game_data['variables']['board_size']['y'] - abs(target_position[1] - current_position[1]))
    
    #Tore isn't needed
    else:
        manhattan_dist = abs(target_position[0] - current_position[0]) + abs(
        target_position[1] - current_position[1])
    return manhattan_dist <= max_range

#---------------------------------------------------------------------------------------------------#

def _make_attacks(attacks_list, game_data):
    """Performs the requested attacks
    Parameters:
    -----------
    attacks_list: list of the attacks that have to be made (list)
    game_data: Dictionary which contain all the informations of the game (dict)
    
    Notes:
    ------
    the list has to be made by "_process_orders"

    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    """
    been_touched = False
    # get the information needed
    for attack in attacks_list:
        damage = attack['power']
        position = attack['target']

        #treat with each player
        for player in game_data['board'][position].copy():
            for ship in game_data['board'][position][player].copy():
                # attack only player's ship
                if player != 0:
                    health = game_data['board'][position][player][ship]['health'] - damage
                    been_touched = True
                    if health <= 0:  # verify if the ship his destroyed
                       # delete the ship from the game
                        del game_data['board'][position][player][ship]
                        if ship in game_data['ships'][player]:
                            del game_data['ships'][player][ship]
                    else:
                        game_data['board'][position][player][ship]['health'] = health

    if not been_touched:
        game_data['variables']['last_damages'] += 1


def _build_board(x_size, y_size, game_board):
    """Build an empty game board.
    Parameters:
    ------------
    x_size: The size of the board in abscissa (int)
    y_size: The size of the board in ordinate (int)
    game_board: empty dict that will contain all the element board (dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 3/03/17)
    """
    
    for x_coordinate in range(1, x_size + 1):
        for y_coordinate in range(1, y_size + 1):
            game_board[(x_coordinate, y_coordinate)] = {0: {}, 1: {}, 2: {}}

#---------------------------------------------------------------------------------------------------#

def _buy_ships(game_data, player1, player2):
    """Ask to the player what he wants to buy.

    Parameters:
    ------------
    game_board: empty dict that will contain all the element of board (dict)

    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    """
    
    player1_orders = ''
    player2_orders = ''

    #verify what is the type of player

    if player1 == 'player':
        player1_orders = raw_input('Player1 - What ship do you want to buy ? :').lower()
    elif player1 == 'remote':
        player1_orders = get_remote_orders()
    else:
        player1_orders = _buy_IA()
    
    #verify what is the type of player
    if player2 == 'player':
        player2_orders = raw_input('Player2 - What ship do you want to buy ? :').lower()
    if player1 == 'remote':
        player2_orders = get_remote_orders()
    else:
        player2_orders = _buy_IA()

    
    _buy_and_add_ships(1, player1_orders, game_data)
    _buy_and_add_ships(2, player2_orders, game_data)

#---------------------------------------------------------------------------------------------------#

def _buy_and_add_ships(player, ships_list, game_data):
    """Place the new ship one the board.

    Parameters:
    ------------
    player: The player who makes the action (int)
    ships_list: The list wich contains all the new ships (list)
    game_board: empty dict that will contain all the element of board (dict)

    Note:
    -----
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hugo Jacques (V.1 3/03/17)
    """
    
    #initialisation of the money of the player
    wallet = 100
    
    #separate all the ship bought
    for ship in ships_list.split(' '):
        #separate the name and the type of the ship
        name, ship_type = ship.split(':')
        #substract the price of the ship
        wallet -= game_data['ship_characteristics'][ship_type]['cost']
        if wallet >= 0:
            _add_ship(player, name, ship_type, game_data)

    game_data['variables']['wallet'][player] = 0

#---------------------------------------------------------------------------------------------------#

def _add_ship(player, ship_name, ship_type, game_data, position=None):
    """Add a ship to a certain position.
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    ship_type: The type of the ship (str)
    game_data: The board and all the informations of the game (dict)
    position: position for the new spaceship (tuple(int, int))

    Notes:
    ------
    The optional parameter "position" is only use when a ship is added with the cis file. Otherwise the position is re-alculated
    Player: it's the player number 0: abandoned, 1:player1, 2:player2

    Note:
    -----
    Player can be 0 for abandonned ship, 1 for player one and 2 for player two

    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    """
    
    ship_name = ship_name.lower()
    
    #give a default orientation
    orientation = 1
    
    #give the information of the position of the ship
    if position == None:
        if player == 1:
            position = game_data['variables']['default_position'][1]
        if player == 2:
            position = game_data['variables']['default_position'][2]
            orientation = 5    
        
    #put the ship in the dictionnary
    game_data['board'][position][player][ship_name] = {'type': ship_type,
                                                       'orientation': orientation,
                                                       'health': game_data['ship_characteristics'][ship_type]['health'],
                                                       'speed': 0}
    game_data['ships'][player][ship_name] = position

#---------------------------------------------------------------------------------------------------#

def _build_from_cis(path, game_data):
    """Build the board and add abandoned ships at the beginning of it from a .cis file
    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: The board and all the informations of the game without the board (dict)

    Version:
    --------
    specification: Elise Hallaert (V.1 3/03/17)
    """
    #open the .cis file
    file_handle = open(path, 'r')
    
    #treat each line of the file
    lines_list = file_handle.readlines()
    board_size = lines_list[0].split(' ')
    
    #get the size of the board
    x_board_size = int(board_size[0])
    y_board_size = int(board_size[1])

    #get the default position of the ships
    game_data['variables']['default_position'] = {}
    game_data['variables']['default_position'][1] = (2, 2)
    game_data['variables']['default_position'][2] = (x_board_size - 1, y_board_size - 1)


    _build_board(x_board_size, y_board_size, game_data['board'])
    #add the information of the board
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

#---------------------------------------------------------------------------------------------------#

def _buy_IA():
    """Gives naive orders to buy some ships
    Version:
    --------
    specification: Elise Hallaert (V.1 31/03/17)
    """ 
    wallet = 100
    action = ''
    name = 'i%d'
    while wallet > 0:
        number = random.randint(1, 99)
        action += name % number
        ship = random.randint(1, 3)
        if ship == 1:
            action += ':fighter'
            wallet -= 10
        elif ship == 2:
            action += ':destroyer'
            wallet -= 20
        else:
            action += ':battlecruiser'
            wallet -= 30
        action += ' '
    return action[:len(action) - 1]

#---------------------------------------------------------------------------------------------------#

def _get_IA_orders(game_data, player):
    """gives naive orders to ships
    
    Parameters:
    ----------
    game_data: The board and all the informations of the game (dict)
    player: number of the player (str)
    
    Notes:
    ------
    Player can be 1 or 2
    
    Version:
    --------
    specification: Elise Hallaert (V.1 31/03/17)
    """
    action = ''
    for ship in game_data['ships'][player]:
        position = game_data['ships'][player][ship]
        if game_data['board'][position][player][ship]['type'] == 'battlecruiser':
        elif game_data['board'][position][player][ship]['type'] == 'fighter':
        elif game_data['board'][position][player][ship]['type'] == 'destroyer':
        for in game_data
            action += ship
            possibility = random.randint(1, 5)
            if possibility == 1:
                action += ':slower '
            elif possibility == 2:
                action += ':faster '
            elif possibility == 3:
                action += ':left '
            elif possibility == 4:
                action += ':right '
            else:
                size_x = game_data['variables']['board_size']['x']
                size_y = game_data['variables']['board_size']['y']
    
                x = random.randint(1, size_x)
                y = random.randint(1, size_y)
    
                action += ':%d-%d ' % (x, y)
    return action[:len(action) - 1]
    ###TEST ZONE###


if __name__ == '__main__':
    print main('C:/Users/Hugo/Desktop/test.cis', 'IA', 'IA')


