def to(x=0, y=0):
	X, Y = get_pos_x(), get_pos_y()
	maxMove = get_world_size() // 2

	xdir, xdis = East, x-X
	if (xdis < 0 and xdis + maxMove > 0) or (xdis > maxMove):
		xdir = West
	if abs(xdis) > maxMove:
		xdis = 	get_world_size() - abs(xdis)
	else:
		xdis = abs(xdis)
	
	ydir, ydis = North, y-Y
	if (ydis < 0 and ydis + maxMove > 0) or (ydis > maxMove):
		ydir = South
	if abs(ydis) > maxMove:
		ydis = get_world_size() - abs(ydis)
	else:
		ydis = abs(ydis)
	
	for i in range(xdis):
		move(xdir)
	for i in range(ydis):
		move(ydir)
