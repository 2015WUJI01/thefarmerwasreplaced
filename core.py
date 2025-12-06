import mv

# 浇水
# 每次只加一次（节约用水，不是），循环种植时就能达到阈值以上，非特殊情况感觉没必要一直加水
def setWater(w):
	if get_water() < w:
		use_item(Items.Water)

# [已弃用] 前期写的单行种植方法，基本只适用于前4种基础作物，高级作物的增产被动完全无法发挥，使用行种植
def harvestAndPlant(rows, p = Entities.Grass, water = 0.4):
	for i in range(rows):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			if p == Entities.Tree:
				if (i+j)%2 == 0:
					plantAny(p, water)
				else:
					plantAny(Entities.Grass, water)
			else:
				plantAny(p, water)
			move(East)
		move(North)

# 种植单颗作物，自动根据阈值管理浇水
# P.S. 实测 0.7 还是有点猛，水科技点满也不够用，0.5应该就够了。最好是不同作物阈值不同，且根据生长速度调整一个大周期内种植的顺序
woodList = [Entities.Tree, Entities.Bush]
def plantAny(pl = Entities.Grass, water = 0.7):
	# 限制浇水
	if pl != Entities.Grass:
		setWater(water)
	# 耕地
	if get_ground_type() != Grounds.Soil:
		till()
	if pl == Entities.Tree:
		pl = woodList[(get_pos_x()+get_pos_y())%2]
	plant(pl)

# 行种植
# 自适应各种作物，特殊规则如下：
# 树：间隔种植灌木，以获取木材
# 南瓜：只种植 6x6 的南瓜，会使用肥料（过渡使用会导致肥料负增长）
def plantRow(x, y, pl, amount = get_world_size()):
	mv.to(x, y)
	for i in range(amount):
		if pl == Entities.Tree:
			target = woodList[(get_pos_x()+get_pos_y())%2]
			if get_entity_type() != target:
				harvest()
			plantAny(target)
		elif get_entity_type() != pl:
			harvest()
			if pl == Entities.Pumpkin:
				if (get_pos_x()+1)%7 != 0 and (get_pos_y()+1)%7 != 0:
					plantAny(pl)
			elif pl == Entities.Cactus:
				#if get_pos_y()%2 != 0:
				plantAny(pl)
			else:
				plantAny(pl)
		move(East)

	if pl == Entities.Cactus:
		for i in range(amount - 1):
			mv.to(x, y)
			swapTimes = 0
			for j in range(amount - 1 - i):
				if (measure() != None and measure() > measure(East)) or measure(East) == None:
					swap(East)
					swapTimes += 1
				move(East)
			if swapTimes == 0:
				break
	
	if pl == Entities.Pumpkin and (get_pos_y()+1)%7 != 0:
		mv.to(x, y)
		# reseed
		for i in range(amount):
			if get_entity_type() == Entities.Pumpkin or get_entity_type() == Entities.Dead_Pumpkin:
				while not can_harvest():
					if get_entity_type() == Entities.Dead_Pumpkin:
						plantAny(Entities.Pumpkin)
					use_item(Items.Fertilizer)
		move(East)


# [已弃用] 初期刷南瓜用，可以直接使用 行种植 plantRow 代替
# 以指定坐标为左下角种植 6x6 的南瓜（会重新种植枯萎作物并使用肥料）
def getBigPumpkin(lbx=0, lby=0):
	mv.to(lbx, lby)
	# seed
	for i in range(6):
		for j in range(6):
			plantAny(Entities.Pumpkin)
			move(East)
		mv.to(lbx, lby + i+1)

	# reseed
	mv.to(lbx, lby)
	for i in range(6):
		for j in range(6):
			while not can_harvest():
				if get_entity_type() == Entities.Dead_Pumpkin:
					plantAny(Entities.Pumpkin)
				use_item(Items.Fertilizer)
			move(East)
		mv.to(lbx, lby + i + 1)
			
	mv.to(lbx, lby)
	harvest()
