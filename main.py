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
    game_board[position_2][player].update({space_ship:game_board[position_1][player][space_ship]}) #CAN BE IMPROVED
    del game_board[position_1][player][space_ship]

def _build_board(game_board, size):
    """Build an empty game board.
        
    Parameters
    -------
    game_board: empty dict that will contain all the element board (dict)
    size: size of the board (x, y size must be the same ????) (tuple (int, int))
    """
    for x in range(1,size+1):
        for y in range(1,size+1):
            game_board[(x, y)] = {0:{}, 1:{}, 2:{}} #build each element of the board (empty dict for player 0,1,2) 

                        
def _add_ship(player, position, ship_info, game_board):
    """Add a ship to a certain position.
        
    Parameters
    -------
    player: is the player's number (0: abandoned, 1:player1, 2:player2) (int)
    position: position for the new spaceship (tuple(int, int))
    ship_info: ship info (see data structure ???) (dict)
    game_board: contains all the game board element (dict)
    """
    game_board[position][player].update(ship_info)
    
 
def _build_from_cis(path, game_data):
    """Build game board from .cis file
        
    Parameters
    -------
    path: path to the cis file (str)
    game_data: game board (dict)
    """
    
    fh = open(path, 'r')
    
    #if not fh:
        #Gestion d'erreur ? 
        
    lines_list = fh.readlines();
    for line in lines_list[1:]:
        line_elements = line.split(' ') #split the line to get each element
        ship_name = line_elements[2].split(':')#split to get the ship name and type
        
        ship_info = {ship_name[0]:{'type': ship_name[1], 'orientation':line_elements[3]}} #build shit info (type, orientation)
        
        _add_ship(0, (int(line_elements[0]), int(line_elements[1])), ship_info, game_data) #cast str to int to get the coordonates
                
                   
 ###TEST ZONE###               
 
                    
                                                 
                         
                            
                                  
game_data ={}
_build_board(game_data, 5)
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)
_move_ship((1,1), (2,2), 0, 'titanic', game_data)
_update_ui(game_data)
#print game_data




