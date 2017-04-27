import random

            
def ship_in_range(goal, player, name, type, game_data):
    opponent_player = 2
    if player == 2:
        opponent_player = 1
    
    ship_position = game_data['ships'][player][name]
    
    if goal =='attack':
        possible_attack = []
        ship_range = game_data['ship_characteristics'][type]['range']
        for x in range (0-ship_range, ship_range):
            for y in range (0-ship_range, ship_range):
                if x + y < ship_range:
                    possible_position = (ship_position[0] + x, ship_position[1] +y)
                    possible_position = apply_tore(possible_position)                   
                    if game_data['board'][possible_position][opponent_player] != {}:
                        possible_attack += possible_position
        if possible_attack ==[]:
            return None
        priority = False
        for possible_position in possible_attack:
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
        choice = random.randint(1,5)
        attack_position = find_five_possibilities(opponent_player, attack_position, game_data,ship_name,ship_type)[choice]
        return attack_position                   
                        
    elif goal =='get_ship':
        ship_possibility = find_five_possibilities(player,ship_position, name, type, True)
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
            
    
def find_five_possibilities(player,position,game_data, name, type, take =False ):
    orientation = game_data['board'][position][player][name]['orientation']
    speed=game_data['board'][position][player][name]['speed']
    max_speed = game_data['ship_characteristics'][type]['max_speed']
    possibilities = []
    opponent_player = 2
    if player == 2:
        opponent_player = 1
    for changement in (-1,0,1):        
        new_speed = speed + changement
        
        if new_speed > 0 and new_speed <= max_speed:
            y_coordinate = position[0]
            x_coordinate = position [1]
            if orientation == 0:        
                y_coordinate -= new_speed        
            elif orientation == 1:        
                x_coordinate += new_speed        
                y_coordinate -= new_speed        
            elif orientation == 2:        
                x_coordinate += new_speed        
            elif orientation == 3:        
                x_coordinate += new_speed        
                y_coordinate += new_speed        
            elif orientation == 4:        
                y_coordinate += new_speed        
            elif orientation == 5:        
                x_coordinate -= new_speed        
                y_coordinate += new_speed        
            elif orientation == 6:        
                x_coordinate -= new_speed        
            elif orientation == 7:        
                x_coordinate -= new_speed        
                y_coordinate -= new_speed
            if take and game_data['board'][(y_coordinate, x_coordinate)][opponent_player]!= {}:
                return ('speed', changement)
                
            possibilities += (y_coordinate,x_coordinate)
    for turn in (-1,1):
        new_orientation = orientation + turn
        new_orientation = new_orientation%8
        y_coordinate = position[0]
        x_coordinate = position [1]
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
        possibilities+=(y_coordinate,x_coordinate)
        if take and game_data['board'][(y_coordinate, x_coordinate)][opponent_player]!= {}:
                return ('orientation', changement)
    return possibilities
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
