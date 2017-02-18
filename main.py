import os

def _build_board(data, size):
    for x in range(1,size+1):
        for y in range(1,size+1):
            data[(x, y)] = {0:{}, 1:{}, 2:{}} #build each element of the board (empty dict for player 0,1,2) 

def _add_ship(player, position, ship_info, game_board):
    game_board[position][player].update(ship_info)
    
 
def _build_from_cis(path, game_data):
    fh = open(path, 'r')
    
    if not fh:
        return 0
        
    lines_list = fh.readlines();
    for line in lines_list[1:]:
        line_elements = line.split(' ') #split the line to get each element
        ship_name = line_elements[2].split(':')#split to get the ship name and type
        
        ship_info = {ship_name[0]:{'type': ship_name[1], 'orientation':line_elements[3]}} #build shit info (type, orientation)
        
        _add_ship(0, (int(line_elements[0]), int(line_elements[1])), ship_info, game_data) #cast str to int to get the coordonates
                
                   
 ###TEST ZONE###                     
                         
                            
                                  
game_data ={}
_build_board(game_data, 40)
_build_from_cis('C:/Users/Hugo/Desktop/test.cis', game_data)

print game_data





