# -*- coding: utf-8 -*-
import random
import socket
import time

def get_IP():
    """Returns the IP of the computer where get_IP is called.

    Returns
    -------
    computer_IP: IP of the computer where get_IP is called (str)

    Notes
    -----
    If you have no internet connection, your IP will be 127.0.0.1.
    This IP address refers to the local host, i.e. your computer.

    """

    return socket.gethostbyname(socket.gethostname())


def connect_to_player(player_id, remote_IP='127.0.0.1', verbose=False):
    """Initialise communication with remote player.

    Parameters
    ----------
    player_id: player id of the remote player, 1 or 2 (int)
    remote_IP: IP of the computer where remote player is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)

    Returns
    -------
    connection: sockets to receive/send orders (tuple)

    Notes
    -----
    Initialisation can take several seconds.  The function only
    returns after connection has been initialised by both players.

    Use the default value of remote_IP if the remote player is running on
    the same machine.  Otherwise, indicate the IP where the other player
    is running with remote_IP.  On most systems, the IP of a computer
    can be obtained by calling the get_IP function on that computer.

    """

    # init verbose display
    if verbose:
        print '\n-------------------------------------------------------------'

    # open socket (as server) to receive orders
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # deal with a socket in TIME_WAIT state

    if remote_IP == '127.0.0.1':
        local_IP = '127.0.0.1'
    else:
        local_IP = get_IP()
    local_port = 42000 + (3 - player_id)

    try:
        if verbose:
            print 'binding on %s:%d to receive orders from player %d...' % (local_IP, local_port, player_id)
        socket_in.bind((local_IP, local_port))
    except:
        local_port = 42000 + 100 + (3 - player_id)
        if verbose:
            print '   referee detected, binding instead on %s:%d...' % (local_IP, local_port)
        socket_in.bind((local_IP, local_port))

    socket_in.listen(1)
    if verbose:
        print '   done -> now waiting for a connection on %s:%d\n' % (local_IP, local_port)

    # open client socket used to send orders
    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # deal with a socket in TIME_WAIT state

    remote_port = 42000 + player_id

    connected = False
    msg_shown = False
    while not connected:
        try:
            if verbose and not msg_shown:
                print 'connecting on %s:%d to send orders to player %d...' % (remote_IP, remote_port, player_id)
            socket_out.connect((remote_IP, remote_port))
            connected = True
            if verbose:
                print '   done -> now sending orders to player %d on %s:%d' % (player_id, remote_IP, remote_port)
        except:
            if verbose and not msg_shown:
                print '   connection failed -> will try again every 100 msec...'
            time.sleep(.1)

            msg_shown = True

    if verbose:
        print

        # accept connection to the server socket to receive orders from remote player
    print 'sutck on accept'
    socket_in, remote_address = socket_in.accept()
    if verbose:
        print 'now listening to orders from player %d' % (player_id)

    # end verbose display
    if verbose:
        print '\nconnection to remote player %d successful\n-------------------------------------------------------------\n' % player_id

    # return sockets for further use
    return (socket_in, socket_out)


def disconnect_from_player(connection):
    """End communication with remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)
    socket_out.shutdown(socket.SHUT_RDWR)

    # close sockets
    socket_in.close()
    socket_out.close()


def notify_remote_orders(connection, orders):
    """Notifies orders of the local player to a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)
    orders: orders of the local player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'

    # send orders
    try:
        socket_out.sendall(orders)
    except:
        raise IOError, 'remote player cannot be reached'


def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # receive orders
    try:
        orders = socket_in.recv(4096)
    except:
        raise IOError, 'remote player cannot be reached'

    # deal with null orders
    if orders == 'null':
        orders = ''

    return orders


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
    Implementation: Hugo Jacques(v.1 12/04/17)
    """

    # initialisation of the main dictionnary
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
                 'variables': {'board_size': {'x': 0, 'y': 0}, 'last_damages': 0}}

    # building of the board
    _build_from_cis(path, game_data)

    # buying of the ships
    _buy_ships(game_data, player_1, player_2)

    # initialisation of the user design
    _update_ui(game_data)

    # connect if playing with remote player
    connection = None
    if player_1 == 'remote':
        connection = connect_to_player(1)
    elif player_2 == 'remote':
        connection = connect_to_player(2)

    # execution of the game
    winner = _game_loop(game_data, player_1, player_2, connection)
    print 'The winner is player %d' % winner


# ---------------------------------------------------------------------------------------------------#

def _game_loop(game_data, player1, player2, connection=None):
    """Execute the game and return the winner when the game is over.

    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)
    player1: type of player (str)
    player2: type of player (str)
    connection: sockets to receive/send orders (tuple, optional)

    Notes:
    ------
    player1 and player2 can be IA, remote or player
    winner can be 1 or 2
    
    Return: 
    -------
    winner: number of the player which has won the game (int)

    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    Implementation: Elise Hallaert (v.1 17/04/17)
    """
    
    # check if the game is ended
    while len(game_data['ships'][1]) > 0 \
            and len(game_data['ships'][2]) > 0 \
            and game_data['variables']['last_damages'] < 10:

        # turn of each type of player
        if player1 == 'IA':
            player1_orders = _get_IA_orders(game_data, 1)
        elif player1 == 'remote':
            player1_orders = get_remote_orders(connection)
        else:
            player1_orders = raw_input('Player1 - What do you want to play ? : ').lower()
        # gives order if playing with remote player
        if player1 == 'IA' and player2 == 'remote':
            notify_remote_orders(connection, player1_orders)

        if player2 == 'IA':
            player2_orders = _get_IA_orders(game_data, 2)
        elif player2 == 'remote':
            player2_orders = get_remote_orders(connection)
        else:
            player2_orders = raw_input('Player2 - What do you want to play ? : ').lower()
        
        # gives order if playing with remote player
        if player1 == 'remote' and player2 == 'IA':
            notify_remote_orders(connection, player2_orders)

        # execute all the actions asked (except the attacks)
        attack_list = _process_order(1, player1_orders, game_data)
        attack_list += _process_order(2, player2_orders, game_data)
        
        # move all the ships
        _move_all_ships(game_data)
        # verify if abandonned ships can be caught
        _get_neutral_ships(game_data)
        # execute the possible attacks
        _make_attacks(attack_list, game_data)
        # update the user design
        _update_ui(game_data)
        # execute the attacks

    # deal with the end of the game
    # deal with the case where 10 turn has passed without any damage
    if game_data['variables']['last_damages'] == 10:

        # initialisation of the players money
        player_money1 = 0
        player_money2 = 0
        # deal with each player
        for player in game_data['ships']:
            # deal with each ship
            for ship in game_data['ships'][player]:
                # get the type of the left ship
                if player != 0:
                    ship_type = game_data['board'][player][ship]['type']

                    # get the price of the type of ship for each player
                    if player == 1:
                        player_money1 += game_data['ship_characteristics'][ship_type]['cost']
                    else:
                        player_money2 += game_data['ship_characteristics'][ship_type]['cost']

            # verify who has won the game
            if player_money1 > player_money2:
                return 1
            elif player_money1 < player_money2:
                return 2
            else:
                # determine the winner randomly
                return random.randint(1, 2)

    # deal with the case where the number of ships is 0
    elif len(game_data['ships'][1]) == 0:
        return 2
    elif len(game_data['ships'][2]) == 0:
        return 1


# ---------------------------------------------------------------------------------------------------#

def _update_ui(game_data):
    """Show the board and the information about the game played

    Parameters:
    -----------
    game_data: dictionary which contains all the information about the game played (dict)

    Version:
    --------
    specification: Métens Guillaume (V.1 5/03/17)
    implementation: Hugo Jacques (v.1 19/04/17)
    """
    
    print ''
    # get board size
    x_size = game_data['variables']['board_size']['x']
    y_size = game_data['variables']['board_size']['y']

    # calculate baord border (to center the board)
    border = (190 - 2 - x_size * 4) / 2
    border_str = ' ' * border
    x_numbers_str = border_str + '   '

    positions_save = {}  # save position that contains ships

    for number in range(1, x_size + 1):
        x_numbers_str += ' \033[4m%02d\033[0m' % (number)
    # initialisation of each player
    ships_informations = {0: '', 1: '', 2: ''}

    # deal with each player
    for player in game_data['ships']:
        # deal with each ship
        for ship in game_data['ships'][player]:
            # get the position of the ship
            position = game_data['ships'][player][ship]
            # get the information of the ship
            ship_info = game_data['board'][position][player][ship]
            # add the information of the ship
            ships_informations[player] += '%s:%s:%s:h%d:o%d:s%d' % (
            ship, position, ship_info['type'], ship_info['health'], ship_info['orientation'],
            ship_info['speed']) + ' - '
            if not position in positions_save:
                positions_save[position] = 0
            positions_save[position] += 1
            
    # print positions_save
    print x_numbers_str

    for row in range(1, y_size + 1):
        line = border_str + ' %02d|' % row

        for column in range(1, x_size + 1):
            if (row, column) in positions_save:
                line += '\033[4m%02d\033[0m|' % positions_save[(row, column)]
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


# ---------------------------------------------------------------------------------------------------#

def _process_order(player, player_orders, game_data):
    """Procces an order asked by a player.

    Parameters:
    -----------
    player: number of the player who is playing (int)
    player_orders: The orders that the player want to process (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Return:
    ------
    attack_list: The list which contains the possible attacks (list)

    Notes:
    ------
    player_orders must have the same syntax than the orders given by the player
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    implementation: Métens Guillaume (v.1 18/04/17)
    """
    
    attack_list = ()
    # split all the string in orders
    for elements in player_orders.split(' '):

        # split each orders in two elements (ship and action)
        action = elements.split(':')

        # verify tat the ship exists or is owned by the player
        if not action[0] in game_data['ships'][player]:
            print 'Error, the ship "%s" does not exist, or is not yours' % (action[0])

        else:
            # deal with each case of action
            if action[1] == 'slower' or action[1] == 'faster':
                _ship_acceleration(player, action[0], action[1], game_data)
            elif action[1] == 'right' or action[1] == 'left':
                _turn_ship(player, action[0], action[1], game_data)
            elif '-' in action[1]:

                # get position to attack
                coord_str = action[1].split('-')
                # get the target
                target = (int(coord_str[0]), int(coord_str[1]))
                # get all the attacks that have to be made
                _check_and_memory_attack(player, action[0], target, attack_list, game_data)
            else:
                print 'The order "%s" can\'t be executed' % action[1]
    return attack_list


# ---------------------------------------------------------------------------------------------------#

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
    implementation: Hallaert Elise (v.1 22/04/17)
    """
    
    # get the position of the ship attacking
    ship_position = game_data['ships'][player][ship_name]
    # get the type of the ship attacking
    ship_type = game_data['board'][ship_position][player][ship_name]['type']
    # verify if the case attacked is in the range of the ship attacking
    if _is_in_range(player, ship_name, attack_position, game_data):
        # add the information of the possible attack
        attacks_list.append(
            {'target': attack_position, 'power': game_data['ship_characteristics'][ship_type]['attack']})


# ---------------------------------------------------------------------------------------------------#

def _move_all_ships(game_data):
    """Move all the ship

    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    Implementation: Hugo Jacques (v.1 15/04/17)
    """
    # make the moves of the ships
    for player in game_data['ships']:
        # deal only with the ships which are not abandonned
        if player != 0:
            for ship_name in game_data['ships'][player]:
                # move the ship
                _move_ship(player, ship_name, game_data)


# ---------------------------------------------------------------------------------------------------#

def _apply_tore(y_coordinate, x_coordinate, game_data):
    """Apply the effect of a tore if the ship is outside the board.

    Parameters:
    -----------
    x_coordinate: The abscissa of the ship (int)
    y_coordinate: The ordinate of the sip (int)
    game_data: Dictionary which contain all the information of the game(dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 4/03/17)
    implementation: Hugo Jacques (v.1 3/04/17)
    """
    #get the information of teh board
    board_x = game_data['variables']['board_size']['x']
    board_y = game_data['variables']['board_size']['y']

    #get the right coordinate
    if x_coordinate > board_x:
        x_coordinate -= board_x
    if y_coordinate > board_y:
        y_coordinate -= board_y

    if x_coordinate < 1:
        x_coordinate += board_x
    if y_coordinate < 1:
        y_coordinate += board_y

    return y_coordinate, x_coordinate


# ---------------------------------------------------------------------------------------------------#

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
    implementation; Hugo Jacques (v.1 5/04/17)
    """
    # deal with each abandonned ship
    for ship in game_data['ships'][0].copy():
        position = game_data['ships'][0][ship]
        player = None

        # treat the cases where the ship can be captured
        if game_data['board'][position][1] and not game_data['board'][position][2]:
            player = 1
        elif not game_data['board'][position][1] and game_data['board'][position][2]:
            player = 2

        # treat the case where the ship is captured
        if player != None:
            if ship in game_data['board'][position][player][ship]:
                new_ship = ship + '_2'
            game_data['board'][position][player][ship] = game_data['board'][position][0][new_ship]
            game_data['ships'][player][ship] = game_data['ships'][0][new_ship]

            del game_data['board'][position][0][ship]
            del game_data['ships'][0][ship]


# ---------------------------------------------------------------------------------------------------#

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
    implementation: Métens Guillaume (v.1 17/04/17)

    """

    # get the position of the ship
    position = game_data['ships'][player][ship_name]
    # get the coordinates of the ship
    y_coordinate = position[0]
    x_coordinate = position[1]

    # get th eorientation of the ship
    orientation = game_data['board'][position][player][ship_name]['orientation']
    # get the speed of the ship
    speed = game_data['board'][position][player][ship_name]['speed']

    # change the position of the ship depending to the speed and the orientation
    new_position = get_new_position (y_coordinate,x_coordinate, speed, orientation)
        
    # change the position of the ship
    game_data['board'][new_position][player][ship_name] = game_data['board'][position][player][ship_name]

    # change the position of the ship
    game_data['ships'][player][ship_name] = new_position


# ---------------------------------------------------------------------------------------------------#

def _turn_ship(player, ship_name, direction_str, game_data):
    """Change the orientation of a ship.

    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    direction_str: Must be left(Anti-clockwise) or right(clockwise) (str)
    game_data: Dictionary which contain all the information of the game (dict)

    Notes:
    ------
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)
    Implementation : Métens Guillaume (v.1 19/04/17)
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


# ---------------------------------------------------------------------------------------------------#

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
    implementation : Métens Guillaume (v.1 21/04/17)
    """

    # Get the current speed and position
    position = game_data['ships'][player][ship_name]
    speed = game_data['board'][position][player][ship_name]['speed']
    # get the max speed of the ship
    max_speed = game_data['ship_characteristics'][game_data['board'][position][player][ship_name]['type']]['max_speed']

    # faster
    if way == 'faster' and speed < max_speed:
        # update the speed of the ship
        game_data['board'][position][player][ship_name]['speed'] += 1
    # slower
    if way == 'slower' and speed > 0:
        # update the speed of the ship
        game_data['board'][position][player][ship_name]['speed'] -= 1


# ---------------------------------------------------------------------------------------------------#

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
    implementation; Hugo Jacques (v.1 17/04/17)
    """
    # get the current position
    current_position = game_data['ships'][player][ship_name]
    # get the type of the ship
    ship_type = game_data['board'][current_position][player][ship_name]['type']
    # get the range of the ship
    max_range = game_data['ship_characteristics'][ship_type]['range']

    # Check if we need to apply "tore" effect
    # Calculate the tore_value:

    # Tore_value_x
    if (game_data['variables']['board_size']['x'] // 2) < (game_data['variables']['board_size']['x'] / 2.0):
        tore_value_x = (game_data['variables']['board_size']['x'] // 2) + 1
    else:
        tore_value_x = (game_data['variables']['board_size']['x'] / 2)

    # Tore_value_y
    if (game_data['variables']['board_size']['y'] // 2) < (game_data['variables']['board_size']['y'] / 2.0):
        tore_value_y = (game_data['variables']['board_size']['y'] // 2) + 1
    else:
        tore_value_y = (game_data['variables']['board_size']['y']) / 2

    # 4 cases => 4 manhattan_dist
    # Tore need to be apply in x AND Y
    if abs(target_position[0] - current_position[0]) >= tore_value_x and abs(
                    target_position[1] - current_position[1]) >= tore_value_y:
        manhattan_dist = (game_data['variables']['board_size']['x'] - abs(target_position[0] - current_position[0])) + (
            game_data['variables']['board_size']['y'] - abs(target_position[1] - current_position[1]))

    # Tore need to be apply in X
    elif abs(target_position[0] - current_position[0]) >= tore_value_x and abs(
                    target_position[1] - current_position[1]) < tore_value_y:
        manhattan_dist = (game_data['variables']['board_size']['x'] - abs(
            target_position[0] - current_position[0])) + abs(target_position[1] - current_position[1])

    # Tore need to be apply in Y
    elif abs(target_position[0] - current_position[0]) < tore_value_x and abs(
                    target_position[1] - current_position[1]) >= tore_value_y:
        manhattan_dist = abs(target_position[0] - current_position[0]) + (
            game_data['variables']['board_size']['y'] - abs(target_position[1] - current_position[1]))

    # Tore isn't needed
    else:
        manhattan_dist = abs(target_position[0] - current_position[0]) + abs(
            target_position[1] - current_position[1])
    return manhattan_dist <= max_range


# ---------------------------------------------------------------------------------------------------#

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
    implementation : Elise Hallaert (v.1 2/04/17)
    """
    been_touched = False
    # get the information needed
    for attack in attacks_list:
        damage = attack['power']
        position = attack['target']

        # treat with each player
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
    else:
        game_data['variables']['last_damages'] = 0


def _build_board(y_size, x_size, game_board):
    """Build an empty game board.
    
    Parameters:
    ------------
    x_size: The size of the board in abscissa (int)
    y_size: The size of the board in ordinate (int)
    game_board: empty dict that will contain all the element board (dict)

    Version:
    --------
    specification: Hugo Jacques (V.1 3/03/17)
    implementation: Métens Guillaume (v.1 5/04/17)
    """

    for y_coordinate in range(1, y_size + 1):
        for x_coordinate in range(1, x_size + 1):
            game_board[(x_coordinate, y_coordinate)] = {0: {}, 1: {}, 2: {}}


# ---------------------------------------------------------------------------------------------------#

def _buy_ships(game_data, player1, player2):
    """Ask to the player what he wants to buy.

    Parameters:
    ------------
    game_board: empty dict that will contain all the element of board (dict)
    player1: type of the player one (str)
    player2: type of the player two (str)
    
    Notes:
    ------
    the type can be IA, remote or player

    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    implementation: Métens Guillaume (v.1 1/04/17)
    
    """

    player1_orders = ''
    player2_orders = ''

    # verify what is the type of player
    if player1 == 'player':
        player1_orders = raw_input('Player1 - What ship do you want to buy ? :').lower()
    elif player1 == 'remote':
        player1_orders = get_remote_orders()
    else:
        player1_orders = _buy_IA()

    # verify what is the type of player
    if player2 == 'player':
        player2_orders = raw_input('Player2 - What ship do you want to buy ? :').lower()
    elif player1 == 'remote':
        player2_orders = get_remote_orders()
    else:
        player2_orders = _buy_IA()

    _buy_and_add_ships(1, player1_orders, game_data)
    _buy_and_add_ships(2, player2_orders, game_data)


# ---------------------------------------------------------------------------------------------------#

def _buy_and_add_ships(player, ships_list, game_data):
    """Place the new ship one the board.

    Parameters:
    ------------
    player: The player who makes the action (int)
    ships_list: The list wich contains all the new ships (list)
    game_data: empty dict that will contain all the element of board (dict)

    Note:
    -----
    Player can be 1 for player one and 2 for player two

    Version:
    --------
    specification: Hugo Jacques (V.1 3/03/17)
    implementation: Elise Hallaert (v.1 21/03/17)
    """

    # initialisation of the money of the player
    wallet = 100

    # separate all the ship bought
    for ship in ships_list.split(' '):
        
        # separate the name and the type of the ship
        if ship:
            name, ship_type = ship.split(':')
            
            # substract the price of the ship
            wallet -= game_data['ship_characteristics'][ship_type]['cost']
            if wallet >= 0:
                _add_ship(player, name, ship_type, game_data)


# ---------------------------------------------------------------------------------------------------#

def _add_ship(player, ship_name, ship_type, game_data, position=None, orientation=None):
    """Add a ship to a certain position.
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    ship_type: The type of the ship (str)
    game_data: The board and all the informations of the game (dict)
    position: position for the new spaceship (tuple(int, int),optional )
    orientation: orientation of the ship (int, optional)

    Notes:
    ------
    The optional parameter "position" is only use when a ship is added with the cis file. Otherwise the position is re-alculated
    Player: it's the player number 0: abandoned, 1:player1, 2:player2

    Note:
    -----
    Player can be 0 for abandonned ship, 1 for player one and 2 for player two
    the orientation can be between 0 and 7

    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    implementation: Métens Guillaume (v.1 02/04/17)
    """

    ship_name = ship_name.lower()

    # give a default orientation
    orientation = 1
    
    # give the information of the position of the ship
    if position == None:
        if player == 1:
            position = game_data['variables']['default_position'][1]
        if player == 2:
            position = game_data['variables']['default_position'][2]
            orientation = 5

            # put the ship in the dictionnary
    game_data['board'][position][player][ship_name] = {'type': ship_type,
                                                       'orientation': orientation,
                                                       'health': game_data['ship_characteristics'][ship_type]['health'],
                                                       'speed': 0}
    game_data['ships'][player][ship_name] = position


# ---------------------------------------------------------------------------------------------------#

def _build_from_cis(path, game_data):
    """Build the board and add abandoned ships at the beginning of it from a .cis file
    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: The board and all the informations of the game without the board (dict)

    Version:
    --------
    specification: Elise Hallaert (V.1 3/03/17)
    implementation: Hugo Jacques (v.1 2/04/17)
    """
    # open the .cis file
    file_handle = open(path, 'r')

    # treat each line of the file
    lines_list = file_handle.readlines()
    board_size = lines_list[0].split(' ')

    # get the size of the board
    y_board_size = int(board_size[0])
    x_board_size = int(board_size[1])

    # get the default position of the ships
    game_data['variables']['default_position'] = {}
    game_data['variables']['default_position'][1] = (10, 10)
    game_data['variables']['default_position'][2] = (y_board_size - 9, x_board_size - 9)

    _build_board(y_board_size, x_board_size, game_data['board'])
    
    # add the information of the board
    game_data['variables']['board_size']['y'] = y_board_size
    game_data['variables']['board_size']['x'] = x_board_size
    for line in lines_list[1:]:
        line_elements = line.split(' ')  # split the line to get each element
        orientation = line_elements[3]
        if orientation == 'up-right':
            orientation = 1
        elif orientation == 'down-left':
            orientation = 5
        elif orientation == 'down-right':
            orientation = 3
        elif orientation == 'up-left':
            orientation = 7
        elif orientation == 'up':
            orientation = 0
        elif orientation == 'down':
            orientation = 4
        elif orientation == 'right':
            orientation = 2
        elif orientation == 'left':
            orientation = 6

        ship_name_type = line_elements[2].split(':')  # split to get the ship name and type

        _add_ship(0,
                  ship_name_type[0],
                  ship_name_type[1],
                  game_data,
                  (int(line_elements[0]),
                   int(line_elements[1])), orientation)  # cast str to int to get the coordonates


# ---------------------------------------------------------------------------------------------------#

def _buy_IA():
    """Give the orders of the IA to buy some ships
    
    Returns:
    --------
    action: action that the IA makes to buy ships (str)
    
    Version:
    --------
    specification: Elise Hallaert (V.1 31/03/17)
    implementation: Hugo Jacques (v.1 6/04/17)
    """
    
    #initialisation of the values
    wallet = 100
    action = ''
    name = 'i%d'
    
    #check if the player can still buy ships
    while wallet > 0:
        
        #gives the name of the ship
        number = random.randint(1, 99)
        action += name % number
        ship = random.randint(1, 3)
        
        #gives the type of the ship
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


# ---------------------------------------------------------------------------------------------------#

def ship_in_range(goal, player, name, kind, game_data):
    """verify if there are ships to attack or to capture in the range
    
    Parameters:
    -----------
    goal: name of the action the ship has to do (str)
    player: number of the current player (int)
    name: name of the ship playing (str)
    kind: type of the ship playing (str)
    game_data: dictionnary which contains the entire game (dict)
    
    Notes:
    ------
    goal can be 'attack' or 'get_ship'
    player can be 1 or 2
    kind can be 'fighter', 'detroyer' or 'battlecruiser'
    
    Version:
    --------
    specifications: Elise Hallaert (v.1 28/04/17)
    implementation: Elise Hallaert (v.1 29/04/17)  
    """
    opponent_player = 2
    if player == 2:
        opponent_player = 1

    ship_position = game_data['ships'][player][name]

    if goal == 'attack':
        possible_attack = []


        if possible_attack == []:
            return None
        priority = False
        print possible_attack
        for possible_position in possible_attack:
            print possible_position
            print possible_attack
            for ship in game_data['board'][possible_position][opponent_player]:
                if game_data['board'][possible_position][opponent_player][ship]['type'] == 'battlecruiser':
                    priority = True
                    ship_priority = possible_position
                    ship_name_priority = ship
                else:
                    attack_position = possible_position
                    ship_name = ship
        if priority:
            attack_position = ship_priority
            ship_name = ship_name_priority

        ship_type = game_data['board'][attack_position][opponent_player][ship_name]['type']
        choice = random.randint(-1, 3)
        attack_position = find_five_possibilities(opponent_player, attack_position, game_data, ship_name, ship_type)[
            choice]
        return attack_position

    elif goal == 'get_ship':
        ship_possibility = find_five_possibilities(player, ship_position, game_data, name, kind, True)
        if ship_possibility[0] == 'orientation':
            if ship_possibility[1] == -1:
                return 'left'
            elif ship_possibility[1] == 1:
                return 'right'
            else:
                return None
        elif ship_possibility[0] == 'speed':
            if ship_possibility[1] == -1:
                return 'slower'
            elif ship_possibility[1] == 1:
                return 'faster'


# ---------------------------------------------------------------------------------------------------#

def find_five_possibilities(player, position, game_data, name, kind, take=False):
    """return five possibilities of position of a ship after the turn of one player
    
    Parameters:
    -----------
    player: number of the player who owns the ship (int)
    position: position of the ship (tuple)
    game_data: dictionnary which contains the entire game (dict)
    name: name of the ship (str)
    kind: type of the ship (str)
    take: say if the player want to capture a ship (bool, optional)
    
    Notes:    
    ------
    player can be 1 or 2
    kind can be 'fighter', 'detroyer' or 'battlecruiser'
    take is True if the player want to capture, False otherwhise
    
    Version:
    --------
    specifications: Elise Hallaert (v.1 28/04/17)
    implementation: Elise Hallaert (v.1 29/04/17)    
    """
    print game_data['board'][position][player][name]['orientation']
    orientation = game_data['board'][position][player][name]['orientation']
    speed = game_data['board'][position][player][name]['speed']
    max_speed = game_data['ship_characteristics'][kind]['max_speed']
    possibilities = []
    opponent_player = 2
    if player == 2:
        opponent_player = 1
    for changement in (-1, 0, 1):
        new_speed = speed + changement

        if new_speed > 0 and new_speed <= max_speed:
            y_coordinate = position[0]
            x_coordinate = position[1]
            temp_pos = get_new_position (y_coordinate, x_coordinate, speed, orientation)
            
            if take and game_data['board'][temp_pos][opponent_player] != {}:
                return ('speed', changement)

            possibilities.append(temp_pos)
    for turn in (-1, 1):
        new_orientation = orientation + turn
        new_orientation = new_orientation % 8
        y_coordinate = position[0]
        x_coordinate = position[1]
        temp_pos = get_new_position (y_coordinate, x_coordinate, speed, orientation)        
        possibilities.append(temp_pos)
        if take and game_data['board'][temp_pos][opponent_player] != {}:
            return ('orientation', changement)
    return possibilities


# ---------------------------------------------------------------------------------------------------#

def fighter_action(player, ship_name, game_data):
    """gives the action of a fighter ship
    
    Parameters:
    -----------
    player: number of the current player(int)
    ship_name: name of the ship playing (str)
    game_data: dictionnay which contains the entire game (dict)
    
    Version:
    --------
    specifications: Elise Hallaert (v.1 28/04/17)
    implementation: Elise Hallaert (v.1 29/04/17) 
    """
    action = ship_name +':'
    position = game_data['ships'][player][ship_name]
    if game_data['board'][position][player][ship_name]['speed'] < 4:
        luck = random.randint(1, 3)
        if luck == 1 or luck == 2:
            action += 'faster '
        else:
            luck = random.randint(1, 2)
            if luck == 1:
                action += 'left '
            else:
                action += 'right '

    elif ship_in_range('get_ship', player, ship_name, 'fighter', game_data) != None:
        action += ship_in_range('get_ship', player, ship_name, 'fighter', game_data) +' '
    elif ship_in_range('attack', player, ship_name, 'fighter', game_data) != None:
        position_to_attack = ship_in_range('attack', player, ship_name, 'fighter', game_data)
        action += str(position_to_attack[0]) + '-' + str(position_to_attack[1]) +' '
    else:
        luck = random.randint(1, 5)
        if luck == 1:
            action += 'slower '
        elif luck == 2:
            action += 'faster '
        elif luck == 3:
            action += 'right '
        elif luck == 4:
            action += 'left '
        elif luck == 5:
            action += 'nothing '
    return action


# ---------------------------------------------------------------------------------------------------#

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
    implementation: Elise Hallaert (v.1 29/04/17)
    """
    action = ''
    for ship in game_data['ships'][player]:

        position = game_data['ships'][player][ship]
        if game_data['board'][position][player][ship]['type'] == 'battlecruiser':
            pass
        elif game_data['board'][position][player][ship]['type'] == 'fighter':
            action += fighter_action(player, ship, game_data)
        elif game_data['board'][position][player][ship]['type'] == 'destroyer':
            action += destroyer_action
    return action[:len(action) - 1]

# ---------------------------------------------------------------------------------------------------#

def get_new_position (y_coordinate, x_coordinate, speed, orientation, game_data):
    """return the new position of a ship after moving
    
    Parameters:
    -----------
    y_coordinate: number of the line of the position (int)
    x_coordinate: number of the column of the position (int)
    speed: speed of the ship (int)
    orientation: orientation of the ship (int)
    game_data: dictionnary which contains all the information of the game (dict)
    
    Notes:
    ------
    orientation can be between 0 and 7
    
    Version:
    --------
    specifications: Elise Hallaert (v.1 28/04/17)
    implementation: Elise Hallaert (v.1 29/04/17)    
    """
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
    temp_pos = _apply_tore(y_coordinate, x_coordinate, game_data)
    
    return temp_pos

# ---------------------------------------------------------------------------------------------------#
        
def destroyer_action (player, ship_name, game_data):
    """gives the action of a destroyer ship
    
    Parameters:
    -----------
    player: number of the current player(int)
    ship_name: name of the ship playing (str)
    game_data: dictionnay which contains the entire game (dict)
    
    Version:
    --------
    specifications: Elise Hallaert (v.1 28/04/17)
    implementation: Métens Guillaume (v.1 30/04/17) 
    """
    
    action = ship_name +':'
    position = game_data['ships'][player][ship_name]
    # Add ship name
    action = ship_name+ ':'

    # If speed < max_speed
    if game_data['board'][position][player][ship_name]['speed'] < game_data['ship_characteristics']['destroyer'][
        'max_speed']:
        # Faster
        action += 'faster '

    # elif neutral ship in range:
    elif ship_in_range('get_ship', player, ship_name, 'destroyer', game_data) != None:
        action += ship_in_range('get_ship', player, ship_name, 'destroyer', game_data)
        action +=' '
    # elif enemy in range
    elif ship_in_range('attack', player, ship_name, 'destroyer', game_data) != None:
        action += ship_in_range('attack', player, ship_name, 'destroyer', game_data)
        action += ' '
    # else
    else:
        # randomly change the speed or the orientation
        possibility = random.randint(1, 4)
        if possibility == 1:
            action += 'slower '
        elif possibility == 2:
            action += 'faster '
        elif possibility == 3:
            action += 'left '
        elif possibility == 4:
            action += 'right '
    return action

main('C:/Users/gmetens/Desktop/coder/test.cis', 'IA', 'IA')
