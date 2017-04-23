def ship_in_range(goal,player, name, type):
    opponent_player = 2
    if player = 2:
        opponent_player = 1
    
    ship_position = game_data['ships'][player][name]
    possible_attack = ()
    if goal =='attack':
        ship_range = game_data['ship_characteristics'][type][range]
        for x in range (0-range, range):
            for y in range (0-range, range):
                posible_position = (ship_position[0] + x, ship_position[1] +y)
                for player in game_data['board'][possible_position]
                    if player != player and game_data['board'][possible_position] != {}:
                        possible_attack += possible_position
        max_number = 1
        for possible_position in possible_attack:
            number = len(game_data['board'][possible_position][opponent_player])
            if number > max_number:
                attack_position = possible_position
                max_number = len(game_data['board'][possible_position][opponent_player])
                
        #choisi une des 5 possibilités au hasard
     return attack_position           
            
                        
    elif goal =='get_ship'
    
def find_five_possibilities(player,position, name, type):
    orientation = game_data['board'][position][player][ship_name]['orientation']
    speed=
