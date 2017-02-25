# -*- coding: utf-8 -*-
import os
import math
def _ship_characteristic(ship_type):
    if ship_type == 'battlecruiser':
        return {'max_speed':1, 'health':20, 'attack':4, 'range':10, 'cost':30}
    elif ship_type == 'destroyer':
        return {'max_speed':2, 'health':8, 'attack':2, 'range':7, 'cost':20}
    elif ship_type == 'fighter':
        return {'max_speed':5, 'health':3, 'attack':1, 'range':5, 'cost':10}
    else:
        print 'error'
        

def _attack_position(position, ship_info, game_board):
    damage = ship_info['damage']
    for player in game_board[position]: #iterate through the players
        for ship in player: #iterate through the player's ship
            ship['health'] -= damage #apply damages
            if ship['health'] <= 0: #verify if the ship his destroyed
                del game_board[position][player] #delete the ship from the game

def _move_ship(position_1, position_2, player, space_ship, game_board):
    """Move the ship of a player to an antoher position
    Parameters:
    ------------
    position_1: The initial position of the ship (tuple(int, int)) #Useless
    position_2: The final position of the ship (tuple(int, int))
    player: The player who makes the move (int)
    space_ship: The name of the ship (str)
    game_board: The board of the game (dict)
    
    Notes:
    ---------
    player: Must be one of this possibilities(0: abandoned, 1:player1, 2:player2)
    """
    #1=up,2=up-right,3=right,4=down-right,5=down;6=down-left,7=left,8=up-left
    #go through the dic to get all the ship names
    for team in range(0,3):
        for elements in game_data['ships'][team]:
            #Get info for each ship
            current_pos = game_data['ships'][team][elements]
            current_speed = game_data['board'][current_pos][team][elements]['speed']
            current_orientation = game_data['board'][current_pos][team][elements]['orientation']
            converted_pos = str(current_pos)
            x = converted_pos[1]
            y = converted_pos[4]
            
            #Move #****SI > BOARD : retirer taille board !! ou x/y <0 : ajouter taille board ========> pour faire un tore************************************************* 
            # A faire vérifier !
            
            if current_orientation == 1:
                y += current_speed
                if y > board_size_y: #Check si dépasse du board
                    y -= board_size_y #Remède au problème et fait "traverser" le board
           
            elif current_orientation == 2:
                #X = ? Y = ?
                if y > board_size_y:
                    y -= board_size_y
                if x > board_size_x:
                    x -= board_size_x
                    
            elif current_orientation == 3:
                x += current_speed
                if x > board_size_x:
                    x -= board_size_x
           
            elif current_orientation == 4:
                #X = ? Y = ?
                if x > board_size_x:
                    x -= board_size_x
                if y < 0:
                    y += board_size_y
          
            elif current_orientation == 5:
                y -= current_speed
                if y < 0:
                    y += board_size_y
           
            elif current_orientation == 6:
                #X = ? Y = ?
                if x < 0:
                    x += board_size_x
                if y < 0:
                    y += board_size_y
          
            elif current_orientation == 7:
                x -= current_speed
                if x < 0:
                    x += board_size_x
           
            elif current_orientation == 8:
                #X = ? Y = ?
                if x < 0:
                    x += board_size_x
                if y > board_size_y:
                    y -= board_size_y
                
    #Update pos...
    #######################################
    
    #pas utilisé / vérif; 
    #game_board[position_2][player].update({space_ship:game_board[position_1][player][space_ship]}) #CAN BE IMPROVED
    #del game_board[position_1][player][space_ship]
  
    
def _turn_ship(space_ship,direction,game_data,player):
    """Change the orientation of a ship
    Parameters:
    ------------
    space_ship: The name of the ship (str)
    direction: Must be right(Anti-clockwise) or left(clockwise) (str)
    game_data: The board and all the informations of the game (dict)
    player: The player who makes the move (int)
    """
    #1=up,2=up-right,3=right,4=down-right,5=down;6=down-left,7=left,8=up-left
    #Get the current direction
    position = game_data['ships'][%d][%s] %(player,space_ship)
    direction = game_data['board'][%s][%d][%s]['orientation'] %(position,player,space_ship)
    
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
    game_data['board'][%s][%d][%s]['orientation'] %(position,player,space_ship) = new_direction


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
    position = game_data['ships'][%d][%s] %(player,space_ship)
    speed = game_data['board'][%s][%d][%s]['speed'] %(position,player,space_ship)
    max_speed = _ship_characteristic(%s) %(game_data['board'][position][player][space_ship]['type']
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
    game_data['board'][%s][%d][%s]['speed'] %(position,player,space_ship) = speed

            
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
    game_data['board'][position][player][ship_name] = {'type':ship_type, 'orientation':'up', 'health':_ship_characteristics(ship_type)['health'], 'speed':0}
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

    _build_board(game_data['board'], int(board_size[0]), int(board_size[1]))

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
 
                    
                                                 
                         
                            
                                  
game_data ={}
_build_board(game_data, 5)
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)
_move_ship((1,1), (2,2), 0, 'titanic', game_data)
_update_ui(game_data)
#print game_data





game_data = {'board': {(1, 1): {0: {}, 1: {}, 2: {}},
           (1, 2): {0: {'Jeanhip': {'health': 20,
                                    'orientation': 1,
                                    'type': 'battlecruiser',
                                    'speed': 1}},
                    1: {},
                    2: {}},
           (1, 3): {0: {}, 1: {}, 2: {}},
           (2, 1): {0: {'Msship': {'health': 20,
                                   'orientation': 2,
                                   'type': 'battlecruiser',
                                   'speed': 1}},
                    1: {},
                    2: {}},
           (2, 2): {0: {}, 1: {}, 2: {}},
           (2, 3): {0: {}, 1: {}, 2: {}},
           (3, 1): {0: {}, 1: {}, 2: {}},
           (3, 2): {0: {}, 1: {}, 2: {}},
           (3, 3): {0: {}, 1: {}, 2: {}}},
 'ships': {0: {'Jeanhip': (1, 2), 'Msship': (2, 1)}, 1: {}, 2: {}}}
for team in range(0,3):
    for elements in game_data['ships'][team]:
        #Get info for each ship
        current_pos = game_data['ships'][team][elements]
        current_speed = game_data['board'][current_pos][team][elements]['speed']
        current_orientation = game_data['board'][current_pos][team][elements]['orientation']
        print current_pos
        positionstr = str(current_pos)
        posX= positionstr[1]
        posY= positionstr[4]
        print positionstr
        print posX,posY



