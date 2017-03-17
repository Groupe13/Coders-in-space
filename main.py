# -*- coding: utf-8 -*-
import pprint
import random
import termcolor

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
    implementation: 
    """
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
                  'variables': {'board_size': {'x': 0, 'y': 0}, 'last_damages': 0, 'wallet': {1: 100, 2: 100}}}

    _buy_ships(game_data)
    _build_from_cis(path, game_data)
    _update_ui(game_data)
    _game_loop(game_data, player_1, player_2)

def _show_game(game_data):
    """Show the board and the information about the game played
    
    Parameters:
    -----------
    game_data: dictionary which contains all the information about the game played (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 5/03/17)
    implementation: 
    """
def _game_loop(game_data,player1,player2):
    """Execute the game and return the winner when the game is over.
    
    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)
    
    Notes:
    ------
    Player can be IA, remote or player
    
    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    implementation: 
    """
    while len(game_data['ships'][1]) > 0 \
            and len(game_data['ships'][2]) > 0 \
            and game_data['variables']['last_damages'] < 10:
        
        if player1 == 'IA':
            player1_orders = _get_IA_orders(game_data)
        elif player1 == 'remote':
            player1_orders = get_remote_control(player)
        else:
            player1_orders = player1_orders = raw_input('Player1 - What do you want to play ? : ').lower()
        
        if player2 == 'IA':
            player2_orders = _get_IA_orders(connection)
        elif player2 == 'remote':
            player2_orders = get_remote_control(connection)
        else:
            player2_orders = raw_input('Player2 - What do you want to play ? : ').lower()        
        
        _make_actions(player1_orders, player2_orders, game_data)  # need to implement it
        _move_all_ships(game_data)
        _get_neutral_ships(game_data)
        _update_ui(game_data)

    if game_data['variables']['last_damages'] == 10:
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


def _update_ui(game_data):
    print ''
    x_size = game_data['variables']['board_size']['x']  # get board size
    y_size = game_data['variables']['board_size']['y']

    border = (190 - x_size * 3) / 2  # calculate baord border (usefull to center the board)
    border_str = ' ' * border
    x_numbers_str = border_str + '   '

    positions_save = {}  # save position that contains boats

    for number in range(1, x_size + 1):
        x_numbers_str += ' \033[4m%02d\033[0m' % (number)

    ships_informations = {0: '', 1: '', 2: ''}

    for player in game_data['ships']:
        for ship in game_data['ships'][player]:
            pos = game_data['ships'][player][ship]
            ship_info = game_data['board'][pos][player][ship]

            ships_informations[player] += '%s:%s:%s:h%d:o%d:s%d' % (
            ship, pos, ship_info['type'], ship_info['health'], ship_info['orientation'], ship_info['speed']) + ' - '
            if not pos in positions_save:
                positions_save[pos] = 0
            positions_save[pos] += 1
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
    line_left = 4
    for p in ships_informations:
        line_size = len(ships_informations[p])
        line_left -= line_size / 190
        print 'Team %d : %s' % (p, ships_informations[p])

    if line_left >= 0:
        for i in range(0, line_left):
            print ''


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
    implementation: 
    """

    orders = player_orders.split(' ')
    for elements in orders:  # split all the str in orders
        action = elements.split(':')  # split each orders in two elements

        if not action[0] in game_data['ships'][player]:  # verify tat the boat exist or is owned by the player
            print 'Error, the ship "%s" does not exist, or is not yours' % action[0]
        else:
            if action[1] == 'slower' or action[1] == 'faster':
                _ship_acceleration(player, action[0], action[1], game_data)
            elif action[1] == 'right' or action[1] == 'left':
                _turn_ship(player, action[0], action[1], game_data)
            elif '-' in action[1]:
                coord_str = action[1].split('-')  # get position to attack
                target = (int(coord_str[0]), int(coord_str[1]))  # cast to str

                _check_and_memory_attack(player, action[0], target,
                                         attacks_list, game_data)  # verify that an attack is possible
                # if it is, it's save to the attacks_list (mutable list)
            else:
                print 'The order "%s" does not exist' % action[1]


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
    implementation: 
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
    """Make all the possible actions asked by the players and the shifting
   
    Parameters:
    -----------
    player1_orders: The orders of the player one (str)
    player2_orders: The orders of the player two (str)
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    implementation: 
    """

    attacks_list = list()
    if player1_orders:
        process_order(1, player1_orders, attacks_list, game_data)
    if player2_orders:
        process_order(2, player2_orders, attacks_list, game_data)

    _make_attacks(attacks_list, game_data)


def _move_all_ships(game_data):
    """Move all the ship
    
    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    implementation: 
    """
    for player in game_data['ships']:
        if player != 0:
            for ship_name in game_datas['ships'][player]:
                _move_ship(player, ship_name, game_data)


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
    implementation: 
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


def _get_neutral_ships(game_data):
    for ship in game_data['ships'][0].copy():
        position = game_data['ships'][0][ship]
        player = None

        if game_data['board'][position][1] and not game_data['board'][position][2]:
            player = 1
        elif not game_data['board'][position][1] and game_data['board'][position][2]:
            player = 2

        if player != None:
            game_data['board'][position][player][ship] = game_data['board'][position][0][ship]
            game_data['ships'][player][ship] = game_data['ships'][0][ship]
            del game_data['board'][position][0][ship]
            del game_data['ships'][0][ship]


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
    implementation: 
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
    game_data: Dictionary which contain all the information of the game (dict)
    
    Note:
    -----
    Player can be 1 for player one and 2 for player two
    
    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)
    implementation: 
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
    implementation: 
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
    implementation: 
    """

    current_position = game_data['ships'][player][ship_name]
    ship_type = game_data['board'][current_position][player][ship_name]['type']
    max_range = game_data['boat_characteristics'][ship_type]['range']

    manhattan_dist = abs(target_position[0] - current_position[0]) + abs(
        target_position[1] - current_position[1])
    return manhattan_dist <= max_range


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
    implementation: 
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
    game_board: empty dict that will contain all the element board (dict)
    
    Version:
    --------
    specification: Hugo Jacques (V.1 3/03/17)
    implementation: 
    """

    for x_coordinate in range(1, x_size + 1):
        for y_coordinate in range(1, y_size + 1):
            game_board[(x_coordinate, y_coordinate)] = {0: {}, 1: {}, 2: {}}


def _buy_ships(game_data, player1, player2):
    """Ask to the player what he wants to buy.
   
    Parameters:
    ------------
    game_board: empty dict that will contain all the element of board (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    implementation: 
    """
    player1_orders = ''
    player2_orders = ''
    if player1 == 'IA':
        player1_orders = raw_input('Player1 - What ship do you want to buy ? :').lower()
    else:
        player1_orders = _buy_IA()

    if player2 == 'IA':
        player2_orders = raw_input('Player2 - What ship do you want to buy ? :').lower()
    else:
        player2_orders = _buy_IA()

    _buy_and_add_ships(1, player1_orders.split(' '), game_data)
    _buy_and_add_ships(2, player_orders.split(' '), game_data)


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
    implementation: 
    """
    wallet = 100

    for ship in ships_list:
        name, ship_type = ship.split(':')
        wallet -= game_data['boat_characteristics'][ship_type]['cost']
        if wallet >= 0:
            _add_ship(player, name, ship_type, game_data)

    game_data['variables']['wallet'][player] = 0


def _add_ship(player, ship_name, ship_type, game_data, position=None):
    """Add a ship to a certain position.
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    ship_type: The type of the boat (str)
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
    implementation: 
    """
    ship_name = ship_name.lower()
    orientation = 1
    if position != None:
        if player == 1:
            position = game_data['variables']['default_position'][1]
        if player == 2:
            position = game_data['variables']['default_position'][2]
            orientation = 5
    else:
        position = position

    game_data['board'][position][player][ship_name] = {'type': ship_type, 'orientation': orientation,
                                                       'health': game_data['boat_characteristics'][ship_type]['health'],
                                                       'speed': 0}
    game_data['ships'][player][ship_name] = position


def _build_from_cis(path, game_data):
    """Build the board and add abandoned ships at the beginning of it from a .cis file
    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: The board and all the informations of the game without the board (dict)
    
    Version:
    --------
    specification: Elise Hallaert (V.1 3/03/17)
    implementation: 
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
    name = 'i'
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

def _get_IA_orders(game_data):
    action = []
    for ship in game_data['ships'][1]:
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
            str(x)
            str(y)
            action += ':' + x + '-' + y + ' '
        return action
            ###TEST ZONE###

if __name__ == '__main__':
    main('test.cis', '', '')

