import random
def _game_loop(dictionnary):
    """
    """
    while (dictionnary['boat_number'][1]>0) and (dictionnary['boat_number'][2]>0) and dictionnary['last_damage']<10:
        answer_one = raw_input('What does player one want to play?')
        answer_two = raw_input('What does player two want to play?')
        _make_action(dictionnary,answer_one, answer_two)
        
    if dictionnary['last_damage'] ==10:
        value = 0
        for player in range [1,2]:
            for ship in dictionnary['ships']:
                position = dictionnary['player']['ship']
                boat_type = ['board'][position][player][ship]
                if player == 1:
                    value_one += dictionnary['characteristics'][boat_type]['cost']
                else:
                    value_two += dictionnary['characteristics'][boat_type]['cost']
        if value_one > value_two:
            return 'player one'
        elif value_two > value_one:
            return 'player two'
        else:
            winner = random.randint(1,2)
            return winner
                
    elif dictionnary['boat_number'][1]==0:
        return 'player two'
    elif dictionnary['boat_number'][2]==0:
        return 'player one'
    
