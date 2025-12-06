import mv
import core
import maze

while True:
	maze.run()

def seed_all(pl):
	mv.to()
	def row():
		x, y = 0, get_pos_y()
		core.plantRow(x, y, pl)
	for _ in range(get_world_size()):
		if pl == Entities.Cactus == 0:
			move(North)
			continue
		if not spawn_drone(row):
			row()
		move(North)
	mv.to()
	while num_drones() != 1:
		do_a_flip()

def harvest_all():
	mv.to()
	def row():
		for _ in range(get_world_size()):
			harvest()
			move(East)
		harvest()
	for _ in range(get_world_size()):
		if not spawn_drone(row):
			row()
		move(North)
	mv.to()
	while num_drones() != 1:
		do_a_flip()

def harvest_cactus():
	mv.to()
	def col():
		for i in range(get_world_size() - 1):
			swapTimes = 0
			mv.to(get_pos_x(), 0)
			for j in range(get_world_size() - 1 - i):
				if (measure() != None and measure() > measure(North)) or measure(North) == None:
					swap(North)
					swapTimes += 1
				move(North)
			if swapTimes == 0:
				break
	for _ in range(get_world_size()):
		if not spawn_drone(col):
			col()
		move(East)
	mv.to()
	while num_drones() != 1:
		do_a_flip()
	harvest()

harvest_all()

harvest_list = [
	Entities.Sunflower,
	Entities.Sunflower,
	Entities.Sunflower,
	Entities.Sunflower,
	Entities.Grass,
	Entities.Grass,
	Entities.Grass,
	Entities.Grass,
	Entities.Tree,
	Entities.Tree,
	Entities.Tree,
	Entities.Carrot,
	Entities.Carrot,
	Entities.Carrot,
	Entities.Carrot,
	Entities.Pumpkin,
	Entities.Pumpkin,
	Entities.Pumpkin,
]

while True:
	for pl in harvest_list:
		seed_all(pl)
		if pl == Entities.Cactus:
			harvest_cactus()
		else:
			harvest_all()
	maze.run()
	maze.run()
