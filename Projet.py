import os

def _build_board(data, size):
    for x in range(1,size+1):
        for y in range(1,size+1):
            data[(x, y)] = {0:{}, 1:{}, 2:{}} #build each element of the board (empty dict for player 0,1,2) 

def _add_ship(player, position, ship_info, game_board):
    game_board[position][player].update(ship_info)
    
 
##def _build_from_cis(path, game_board):
    
       
          
             
                
                   
 ###TEST ZONE###                     
                         
                            
                                  
game_data ={}
_build_board(game_data, 40)
fh = open('C:/Users/TEST/Desktop/test.cis', 'r')

lines_list = fh.readlines()
for line in lines_list[1:]: #process each line
        line_element = line.split(' ') #split the line to get each element
        ship_name = line_element[2].split(':')#split to get the ship name and type
        ship_info = {ship_name[0]:{'type': ship_name[1], 'orientation':line_element[3]}} #build shit info (type, orientation)
        _add_ship(0, (int(line_element[0]), int(line_element[1])), ship_info, game_data)
        print game_data[(int(line_element[0]), int(line_element[1]))]

fh.close()




