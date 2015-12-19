
from __future__ import division

from visual import *

import random
from math import sin, cos

debug = True
rowlabel = "ABCDEFGHIJ"
shipL = [5, 4, 3, 3, 2]

def make_pegs(row, col):
	"""makes pegs that will represent the board"""
	
	peg = cylinder(pos=(row-4.75, -3, col-6), axis=(0,0.1,0), radius=0.3, color=color.gray(0.8))

	return peg

def make_oppships(shipL):
	"""makes ships that will occupy your board
	shipL is a list of lists of two integers in the format [R,C]"""

	for pegs in shipL:

		R = deconstructPin(pegs)[0]
		C = deconstructPin(pegs)[1]

		box(pos=(C-4.75, -3, R-10), length=0.8, height = 0.6, width = 0.8, color=color.orange)

def make_myships(shipL):
	"""makes ships that will occupy your board"""

	for pegs in shipL:

		R = deconstructPin(pegs)[0]
		C = deconstructPin(pegs)[1]

		box(pos=(C-4.75, -3, R+1), length=0.8, height = 0.6, width = 0.8, color=color.blue)

def make_missiles(player, pin):
	"""makes missiles that will hit the pegs. player 1 is opponent, 2 is you"""

	pinC = deconstructPin(pin)[0]

	if player == 1:
		missile = sphere(pos=(pinC-4.75, -2.8, -11), radius=0.3, color=color.red)
	else:
		missile = sphere(pos=(pinC-4.75, -2.8, 12.5), radius=0.3, color=color.blue)

	return missile

def remove_ship(pin):
	"""removes ship peg from the board"""

	R = deconstructPin(pin)[0]
	C = deconstructPin(pin)[1]

	box(pos=(C-4.75, -3, R+1), length=0.8, height = 0.3, width = 0.8, color=(0.47, 0.57, 0.67))

def make_arena():
	"""creates vPython board"""

	scene_main = display(title = 'Battleship', x= 0, y=0, width=800, fov=10*(pi/180),\
		height = 600, autoscale = 0, range = (18, 5, 15), center = (0,2,0), forward = (0,-10,0))
	
	ground = box(pos=(0.25, -3, 0), length = 25, width= 25, height=0.1, color = (0.47, 0.57, 0.67))

	for row in range(10):
		for col in range(-4, 6):
			make_pegs(row, col)

	for row in range(10):
		for col in range(7,17):
			make_pegs(row,col)

	wall = box(pos=(-0.25, -0.5, 0), length = 11, width = 0.6, height = 5, color=(1,1,1))   # separating wall

	labelC = text(text = "0   1   2   3   4   5   6   7   8   9", pos=(-0.25, -2.8, 11.25),\
	 font = 'sans', height=0.5, align='center', depth = -0.1, axis= (1,0,0), color = color.white, up = (0,0,-1))  # column labels

	labelR = text(text = "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ", pos=(5.25, -2.8, 1.2),\
		font = 'sans', height=0.5, align='center', vertical_spacing = 1,depth = -0.1, axis= (1,0,0), color = color.white, up = (0,0,-1))  # row labels

	labelC2 = text(text = "0   1   2   3   4   5   6   7   8   9", pos=(-0.25, -2.8, -11),\
	 font = 'sans', height=0.5, align='center', depth = -0.1, axis= (1,0,0), color = color.white, up = (0,0,-1))

	labelR2 = text(text = "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ", pos=(5.25, -2.8, -9.75),\
		font = 'sans', height=0.5, align='center', vertical_spacing = 1,depth = -0.1, axis= (1,0,0), color = color.white, up = (0,0,-1))

def createBoard():
	"""Creates 2D Battleship board, shown through terminal"""

	gameB = []

	for row in range(10):
		gameB += [[' O '] * 10]

	return gameB

def boardString(gameB):
	"""Creates 2D representation of the board on terminal"""

	boardS = " "

	for col in range(10):
		boardS += str(col) + "  "		# columns labeled using integers 0-9
	boardS += "\n" + 31 * "-" + "\n"

	for row in range(10):
		for col in range(10):
			boardS += gameB[col][row]
		boardS += "| " + rowlabel[row] + "\n" 	# rows labeled using alphabets A-J

	print boardS

def addShip(gameB, pin):
	"""adds a pin to the 2D board using a string of the format column (int) - row (letter)"""

	row = deconstructPin(pin)[1]
	col = deconstructPin(pin)[0]

	gameB[row][col] = ' X ' 		# places a marker for an added peg

	return gameB

def labelBoard():
	"""create a list of pin labels in string UI form of col - row"""

	boardS = []

	for rows in range(10):
		for cols in range(10):
			boardS += [createPin(cols, rows)]

	return boardS

def createPin(C, R):
	"""Creates the pin string for a ship using row and column integers in
	the form column (letter) - row (int)"""

	pinC = rowlabel[C]
	pinR = R

	pinS = pinC + str(pinR)

	return pinS

def deconstructPin(pin):
	"""Converts from string to integer indices in a list in form [letter index, int index]"""

	pinC = rowlabel.index((pin[0][0]).upper())	# upper() eliminates case-sensitivity
	pinR = int(pin[1])

	pinL = [pinC, pinR]

	return pinL

def checkV(l, h, gameB):
	"""Checks if ship of length l can be placed vertically
	with the head on h on the board. returns a boolean, true if ship can be placed.
	helper function for setting boards"""

	pins = 0
	check = False

	try:
		while pins < l:			# loops for the length of the ship

			if gameB[ h[1] ][ h[0] + pins ] == ' O ':		# checks if position is occupied
				pins += 1 
				check = True
			else:
				check = False
				break

	except IndexError: 			# breaks loop if IndexError occurs
		check = False

	return check

def checkH(l, h, gameB):
	"""Checks if ship of length l can be placed horizontally
	with the head on h on the board. returns a boolean, true if ship can be placed.
	helper function for setting boards"""

	pins = 0
	check = False

	try:
		while pins < l: 		# loops for the length of the ship

			if gameB[ h[1] + pins ][ h[0]] == ' O ': 		# checks if position is occupied
				pins += 1
				check = True
			else:
				check = False
				break

	except IndexError: 			# breaks loop if IndexError occurs
		check = False

	return check

def setMy(gameB):
	"""sets ships for the user based on prompted answers
	it must check that the user is inputting valid pin values
	each input is a head pin of the ship
	another prompt asks for the direction of the ship (vertical / horizontal)"""

	print "Your board looks like this. Each peg has a name in the format 'A0'. "
	boardString(gameB) 		# prints user's board

	myShips = []

	i = 0

	while i < len(shipL): 		# loops until 5 ships are all placed

		try:
			shipS = (raw_input("Enter the head peg for ship of length %d in the format 'A0': " % (shipL[i]))).upper() # ignores case-sensitivity
		
			try:
				direct = (raw_input("What direction would you like to place this in? (v for vertical, h for horizontal) ")).lower() # ignores case-sensitivity
				shipP = deconstructPin(shipS)
			
				if direct == "v" and not checkV(shipL[i], shipP, gameB): 		# if direction is vertical, but placement is not possible
					print "Vertical placement error. Try another peg."
					continue

				if direct == "h" and not checkH(shipL[i], shipP, gameB): 		# if direction is horizontal, but placement is not possible
					print "Horizontal placement error. Try another peg."
					continue

				if direct == "h":	
					pins = 0
					while pins < shipL[i]:		# loops for length of the ship

						addShip(gameB, createPin(shipP[0], shipP[1] + pins)) 	# adds the ship to the 2D board
						myShips += [createPin(shipP[0], shipP[1] + pins)] 	# adds ship to the temporary solution key
						pins += 1

					i += 1

				if direct == "v":
					pins = 0
					while pins < shipL[i]: 		# loops for the length of the ship

						addShip(gameB, createPin(shipP[0] + pins, shipP[1])) 	# adds the ship to the 2D board
						myShips += [createPin(shipP[0] + pins, shipP[1])] 	# adds the ship to the temporary solution key
						pins += 1

					i += 1

				if direct != "h" and direct != "v":
					print "Weird direction. Enter either 'v' for vertical or 'h' for horizontal. Try again!"
					continue

			except ValueError or IndexError: 		# if an IndexError occurs, loop continues after prompting for a different peg
				print "Ship must stay within bounds of the board. Try another peg."
				continue
		except:
			print "Ship must stay within bounds of the board. Try another peg."
			continue
				
		boardString(gameB) 			# current board is printed

	print "Great! Now let's start the game."

	return myShips

def setOpp():
	"""Creates a set of ships for the computer/opponent"""

	oppB = createBoard()
	oppShips = []

	i = 0

	while i < len(shipL): 		# runs loop until all 5 ships are placed
	
		headpin = [random.randint(0,9-shipL[i]),random.randint(0,9-shipL[i])] 		# generates a random head pin to be placed

		v = checkV(shipL[i], headpin, oppB) 		# runs vertical placement check
		h = checkH(shipL[i], headpin, oppB)		# runs horizontal placement check

		if v and h:			# if both vertical and horizontal placements are possible
			
			choice = random.randint(0,1) 		# random direction is chosen

			if choice == 0:
				for pins in range(shipL[i]):

					oppB[ headpin[1] ][ headpin[0] + pins ] = ' X ' 
					oppShips += [createPin( headpin[1], headpin[0] + pins )]
				
				i += 1

			else:
				for pins in range(shipL[i]):
					oppB[ headpin[1] + pins ][ headpin[0] ] = ' X '

					oppShips += [createPin( headpin[1] + pins , headpin[0] )]
				
				i += 1

		if v and not h:			# vertical placement

			for pins in range(shipL[i]):
					oppB[ headpin[1] ][ headpin[0] + pins ] = ' X '

					oppShips += [createPin( headpin[1], headpin[0] + pins )]
			
			i += 1

		if not v and h: 		# horizontal placement

			for pins in range(shipL[i]):
					oppB[ headpin[1] + pins ][ headpin[0] ] = ' X '

					oppShips += [createPin( headpin[1]+ pins , headpin[0] )]
			
			i += 1


	return oppShips

def nested(L):

	"""helper function that creates a nested list of ships for view on terminal"""

	nested = []

	incr = 0

	for index in range(len(shipL)):

		nested += [ L[incr : incr + shipL[index]] ]
		incr += shipL[index]

	return nested

def tryMove(ships, attempt):
	"""if a ship is hit, returns true. attempt is a string denoting a pin"""

	if attempt in ships:
		return True

	return False

def shoot_oppmissile(m, pin):
	"""shoots the opponent missile at pin"""

	pinL = deconstructPin(pin)

	g = 9.8 #m/s

	initialVel = 15
	angle = -1.297 * pinL[0] + 88.986   # general equation used to determine angle based on directed peg
	angle = angle * (pi/180)

	VelY = initialVel*sin(angle)
	VelX = initialVel*cos(angle)

	t = 0
	dt = 0.01

	while True:
		rate(200)
		t += dt

		mY = -2.8 + VelY*t - 0.5* g*t**2 		# kinematics !!!
		mX = VelX * t

		m.pos = vector(pinL[1]-4.75, mY, mX)

		if mY + 2.8 <= 0:
			break

def shoot_mymissile(m, pin):
	"""shoots the opponent missile at pin"""

	pinL = deconstructPin(pin)

	g = 15 #m/s

	initialVel = 25
	angle = 0.75 * pinL[0] + 75.25		# note here that the equation to pinpoint the peg's destination is different here
	angle = angle * (pi/180)

	VelY = initialVel*sin(angle)
	VelX = initialVel*cos(angle)

	t = 0
	dt = 0.01

	while True:
		rate(200)
		t += dt

		mY = -2.8 + VelY*t - 0.5* g*t**2
		mX = VelX * t

		m.pos = vector(pinL[1]-4.75, mY, -mX+10.5)

		if mY + 2.8 <= 0:
			break

def playGame():
	"""plays the game"""

	print "Welcome to Battleship."
		
	gameB = createBoard()

	myShips = setMy(gameB)
	oppShips = setOpp()

	make_arena()

	for ship in nested(myShips):
		make_myships(ship)

	if debug:
		print "GRUTOR MODE -- Your ships: "
		print nested(myShips)

	if debug:
		print "GRUTOR MODE -- Opponent ships: "
		print nested(oppShips)

		for ship in nested(oppShips):
			make_oppships(ship)

	oppBoard = labelBoard()

	while len(oppShips) != 0 and len(myShips) != 0:
		try:
			attempt = (raw_input("Your turn. Take a shot! (Enter peg in format the 'A0'): ")).upper()
			mMy = make_missiles(2, attempt) 	# initialization of missile location

		except ValueError or IndexError:		# validation for correct peg input
			print "That's not a valid peg. Try again."
			continue

		shoot_mymissile(mMy, attempt)			# animated missile movement

		if tryMove(oppShips, attempt):

			oppShips.remove(attempt)			# keeps track of which ships are hit

			print "Nicely done -- That's a hit!"

			mMy.visible = False
			box(pos=(deconstructPin(attempt)[1]-4.75, -3, deconstructPin(attempt)[0]-10), length=0.8, height = 1, width = 0.8, color=color.red)

			if debug:
				print "GRUTOR MODE -- Remaining opponent ships: "
				print nested(oppShips)

		else:
			print "Miss! Try again."

		if len(oppShips) == 0:

			text(text = "WIN!", pos=(0, 5, 5), font = 'sans', height=10, align='center',\
				depth = -0.3, axis= (1,0,0), color = color.yellow, up = (0,0,-1))

			print "You win!"
			break

		print "Opponents turn. Here goes--"
		oppA = random.choice(oppBoard)			# random pin is chosen

		mOpp = make_missiles(1, oppA) 			# initalization of missile location

		shoot_oppmissile(mOpp, oppA)

		if tryMove(myShips, oppA):

			oppBoard.remove(oppA)				# makes sure the computer does not choose the same peg twice
			box(pos=(deconstructPin(oppA)[1]-4.75, -3, deconstructPin(oppA)[0]+1), length=0.8, height = 1, width = 0.8, color=(0.47, 0.57, 0.67))

			print "It's a hit! You've lost %s" % (oppA)

		else:

			oppBoard.remove(oppA)

			print "Computer misses."

		if len(myShips) == 0:

			text(text = "LOSE :(", pos=(0, 5, 5), font = 'sans', height=6, align='center',\
				depth = -0.3, axis= (1,0,0), color = color.red, up = (0,0,-1))

			print "You lose. Better luck next time!"
			break


def main():
	"""main function"""

	while True:
		playGame()

		again = (raw_input("Would you like to play again? (y/n) ")).lower()

		if again == "y":
			continue
		else:
			print "Bye!"
			break



if __name__ == "__main__": 
    main()                






