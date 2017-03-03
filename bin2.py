def _apply_tore(x, y, game_data):
    """"""
    board_x = game_data['const']['board_size'][0]
    board_y = game_data['const']['board_size'][1]
    if x > board_x:
        x -= board_x
    if y > board_y:
        y -= board_y

    if x < board_x:
        x += board_x
    if y < board_y:
        y += board_y

    return x, y


def _move_ship(ship_name, player, game_data):
    position = game_data['ships'][player][ship_name]
    print position
    x = position[0]
    y = position[1]

    orientation = game_data['board'][position][player][ship_name]['orientation']
    speed = game_data['board'][position][player][ship_name]['speed']

    if orientation == 0:
        y -= speed
    elif orientation == 1:
        x += speed
        y -= speed
    elif orientation == 2:
        x += speed
    elif orientation == 3:
        x += speed
        y += speed
    elif orientation == 4:
        y += speed
    elif orientation == 5:
        x -= speed
        y += speed
    elif orientation == 6:
        x -= speed
    elif orientation == 7:
        x -= speed
        y -= speed

    new_position = _apply_tore(x, y, game_data)

    game_data['board'][new_position][player][ship_name] = game_data['board'][position][player][ship_name]
    del game_data['board'][position][player][ship_name]

    game_data['ships'][player][ship_name] = new_position
