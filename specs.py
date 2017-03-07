def _process_order(player, player_orders, attaks_list, game_data):
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
    attacks_list 
    
    Version:
    --------
    specification: Hugo Jacques (V.1 5/03/17)
    implementation: 
    """

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
    
    Version:
    --------
    specification: Hallaert Elise (V.1 5/03/17)
    implementation: 
    """
    
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

def _game_loop(game_data):
    """Execute the game and return the winner when the game is over.
    
    Parameters:
    -----------
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Elise Hallaert (V.1 4/03/17)
    implementation: 
    """

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
 
def _move_ship(player, ship_name, game_data):
    """Move the ship of a player to a new position.
    
    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)
    implementation: 
    """
 
def _turn_ship(player, ship_name, direction_str, game_data):
    """Change the orientation of a ship.
   
    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    direction_str: Must be left(Anti-clockwise) or right(clockwise) (str)
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 4/03/17)
    implementation: 
    """

def _ship_acceleration(player, ship_name, way, game_data):
    """Change the speed of a ship.
    
    Parameters:
    ------------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    way: Must be slower or faster (str)
    game_data: Dictionary which contain all the information of the game (dict)
    
    Version:
    --------
    specification: Hugo Jacques (V.1 4/03/17)
    implementation: 
    """
 
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
    
    Version:
    --------
    specification: Métens Guillaume (V.1 5/03/17)
    implementation: 
    """
    
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

def _add_ship(player, ship_name, ship_type, game_data, position=(1, 1)):
    """Add a ship to a certain position.

    Parameters:
    -----------
    player: The player who makes the action (int)
    ship_name: The name of the ship (str)
    ship_type: The type of the boat (str)
    position: position for the new spaceship (tuple(int, int))
    game_data: The board and all the informations of the game (dict)
    
    Version:
    --------
    specification: Métens Guillaume (V.1 3/03/17)
    implementation: 
    """
    
def _build_board_from_cis(path, game_data):
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
