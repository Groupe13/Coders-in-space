def _make_action(dictionnary, 
def _game_loop(dictionnary):
    """Start the game until the end
    Parameters:
    -----------
    dictionnary: dictionnary which contain the informations of the game
    """
def main(path):
    """principal function which contain the game
    Parameters:
    -----------
    path: path of the .cis file which contains information to play  
    """
def _ship_characteristic(ship_type):
    """return a dictionnary of information for a type of boat
    
    Parameters:
    -----------
    ship_type: type of the boat whose we want the informations (str)
    
    Return:
    -------
    dico: dictionnary which contain the informations for a type of boat (dictionnary)
    
    Notes:
    ------
    gives all the informations for a type of boat
    """
    

def _attack_memory(boat_name, player, attack_position):
    """Returns a list of the attacks that can be made
    parameters:
    -----------
    boat_name: name of the boat that has to attack (str)
    player: number of the player who is playing (int)
    position_attack: place where the boat has to attack (tuple)
    
    Return:
    -------
    attack_list: list of the attacks that can be made (list)
    """

def _move_ship(boat_name, player):
    """Move the ship of a player to an antoher position
    Parameters:
    -----------
    boat_name: name of the boat who is moving (str)
    player: The player who makes the move (int) 
    
    
    Notes:
    ------
    player: Must be one of this possibilities(0: abandoned, 1:player1, 2:player2)
    """

def _build_board(game_board, size):
    """Build an empty game board.
        
    Parameters:
    ------------
    game_board: empty dict that will contain all the element board (dict)
    size: size of the board (x, y size must be the same ????) (tuple (int, int))
    """
                        
def _add_ship(player, position, ship_info, game_board):
    """Add a ship to a certain position.
        
    Parameters:
    -----------
    player: is the player's number (0: abandoned, 1:player1, 2:player2) (int)
    position: position for the new spaceship (tuple(int, int))
    ship_info: ship info (see data structure ???) (dict)
    game_board: contains all the game board element (dict)
    """
    game_board[position][player].update(ship_info)
    
def _build_from_cis(path, game_data):
    """Build game board from .cis file
        
    Parameters:
    ------------
    path: path to the cis file (str)
    game_data: game board (dict)
    """
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
    
def _is_in_range(ship_position, attack_position):
    """Verify is the case attacked is in the range of the boat
    Parameters:
    -----------
    ship_position: position of the ship which has to attack (tuple)
    attack_position: coordonate of the case that the boat has to attack (tuple)
        
    Returns:
    --------    
    in_range: if the place can be attacked or not (bool)
    
    Notes:
    ------
    in_range is True if the case can be attacked, False otherwhise
    """
def _make_attack (attack_list):
    """makes the attacks that cvan be made
    Parameters:
    -----------
    attack_list: list of the attacks that can be made (list)
    
    Notes:
    ------
    the list has to be made by "_attack_memory" 
    """                                                            
