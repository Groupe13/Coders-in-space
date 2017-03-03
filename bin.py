

def _move_ship(position_1, position_2, player, space_ship, game_board):

    for team in range(0, 3):
        for elements in game_data['ships'][team]:
            # Get info for each ship
            current_pos = game_data['ships'][team][elements]
            current_speed = game_data['board'][current_pos][team][elements]['speed']
            current_orientation = game_data['board'][current_pos][team][elements]['orientation']
            converted_pos = str(current_pos)
            x = converted_pos[1]
            y = converted_pos[4]
            if current_orientation == 1:
                y += current_speed
                if y > board_size_y:  # Check si dépasse du board
                    y -= board_size_y  # Remède au problème et fait "traverser" le board

            elif current_orientation == 2:
                # X = ? Y = ?
                if y > board_size_y:
                    y -= board_size_y
                if x > board_size_x:
                    x -= board_size_x

            elif current_orientation == 3:
                x += current_speed
                if x > board_size_x:
                    x -= board_size_x

            elif current_orientation == 4:
                # X = ? Y = ?
                if x > board_size_x:
                    x -= board_size_x
                if y < 0:
                    y += board_size_y

            elif current_orientation == 5:
                y -= current_speed
                if y < 0:
                    y += board_size_y

            elif current_orientation == 6:
                if x < 0:
                    x += board_size_x
                if y < 0:
                    y += board_size_y

            elif current_orientation == 7:
                x -= current_speed
                if x < 0:
                    x += board_size_x

            elif current_orientation == 8:
                if x < 0:
                    x += board_size_x
                if y > board_size_y:
                    y -= board_size_y
