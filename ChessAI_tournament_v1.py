import math	
import copy
import time

#Default names of text files to read and write to
fileWrite = "gameResult.txt"
fileRead = "testCase.txt"

alpha = float("-infinity")
beta = float("infinity")

output = open(fileWrite, "w")


def read(fileRead):
	f = open(fileRead, "r")
	temp = []
	for line in f:
		if line[0] == "x":
			temp.append((line[0].upper(), "W"+line[2], int(line[4])-1, int(line[6])-1))
		else:
			temp.append((line[0].upper(), "B"+line[2], int(line[4])-1, int(line[6])-1))
		#temp.append((line[0], line[2], int(line[4])-1, int(line[6])-1))

	f.close()
	return temp

class Piece:
	def __init__(self):
		self.player = None
		self.ptype = None
		self.x = None
		self.y = None
		self.capture = False

	def setValue(self,player,ptype,x,y):
		self.player = player
		self.ptype = ptype
		self.x = x
		self.y = y

	def updatePos(self,x,y):
		self.x = x
		self.y = y

	def getPos(self):
		return (self.x,self.y)

	def printPiece(self):
		output.write(self.player + self.ptype + "(" + self.x + "," + self.y +")\n")
		print(self.player,self.ptype,"(",self.x,",",self.y,")")

	def getSurrounding(self):
		temp= [(self.x+1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1), (self.x, self.y+1), (self.x, self.y-1), (self.x+1, self.y), (self.x-1, self.y)]
		temp = [x for x in temp if x[0]>=0 and x[0]<=7]
		temp = [x for x in temp if x[1]>=0 and x[1]<=7]
		return temp

def rookway(piece):
	locations = []
	for i in range(0,8):
		if (i,piece.y) != (piece.x,piece.y):
			locations.append((i, piece.y))
		if (piece.x,i) != (piece.x,piece.y):
			locations.append((piece.x, i))
	return locations

class Board:
	def __init__(self):
		self.WK = Piece()
		self.WR = Piece()
		self.BK = Piece()

	def addPiece(self,player,ptype,x,y):
		if(player == "X"):
			if(ptype == "WK"):
				self.WK.setValue(player,ptype,x,y)
			else:
				self.WR.setValue(player,ptype,x,y)
		else:
			self.BK.setValue(player,ptype,x,y)

	def printState(self):
		printBoard(self.WK,self.WR, self.BK)

	def availablePos(self,piece):
		available = []
		result = []
		dangerZone = []
		size =0
		if piece.player == "X":
			dangerZone = self.BK.getSurrounding()
			if piece.ptype == "WK":
				available = self.WK.getSurrounding()
				if self.WR.capture == False:
					if (self.WR.x,self.WR.y) in available:
						available.remove((self.WR.x,self.WR.y))
			elif piece.ptype == "WR" and piece.capture == False:
				available = rookway(piece)
				if (self.WK.x,self.WK.y) in available:
					available.remove((self.WK.x,self.WK.y))
				if self.WK.x == self.WR.x:
					if self.WK.y < self.WR.y:
						size = len(available)
						for i in range(size):
							for temp in available:
								if temp[1]<self.WK.y:
									available.remove(temp) 
					elif self.WK.y > self.WR.y:
						zize = len(available)
						for i in range(size):
							for temp in available:
								if temp[1]<self.WK.y:
									available.remove(temp) 
				if self.WK.y == self.WR.y:
					if self.WK.x < self.WR.x:
						size = len(available)
						for i in range(size):
							for temp in available:
								if temp[0]<self.WK.x:
									available.remove(temp) 
					elif self.WK.x > self.WR.x:
						zize = len(available)
						for i in range(size):
							for temp in available:
								if temp[0]>self.WK.x:
									available.remove(temp) 
		elif piece.ptype == "BK":
			available = self.BK.getSurrounding()
			dangerZone = self.WK.getSurrounding()
			if self.WR.capture == False:
				dangerZone.extend(rookway(self.WR))
				if self.WK.x == self.WR.x:
					if self.WK.y < self.WR.y:
						size = len(dangerZone)
						for i in range(size):
							for temp in dangerZone:
								if temp[1]<self.WK.y:
									dangerZone.remove(temp) 
					elif self.WK.y > self.WR.y:
						zize = len(dangerZone)
						for i in range(size):
							for temp in dangerZone:
								if temp[1]<self.WK.y:
									dangerZone.remove(temp) 
				if self.WK.y == self.WR.y:
					if self.WK.x < self.WR.x:
						size = len(dangerZone)
						for i in range(size):
							for temp in dangerZone:
								if temp[0]<self.WK.x:
									dangerZone.remove(temp) 
					elif self.WK.x > self.WR.x:
						zize = len(dangerZone)
						for i in range(size):
							for temp in dangerZone:
								if temp[0]>self.WK.x:
									dangerZone.remove(temp)

		size = len(available)
		for i in range(size):
			for temp in available:
				if temp in dangerZone:
					available.remove(temp) 

		for i in available:
			result.append((piece.ptype, i[0], i[1]))
		return result

	def legalMove(self,piece):
		locations = []
		for i in range(0,8):
			if (i,piece.y) != (piece.x,piece.y):
				locations.append((i, piece.y))
			if (piece.x,i) != (piece.x,piece.y):
				locations.append((piece.x, i))

		if self.WR.x == self.WK.x:
			size = len(locations)
			for i in range(size):
				for temp in locations:
					if self.WR.y < self.WK.y:
						if temp[1]>self.WK.y:
							locations.remove(temp)
					else:
						if temp[1]<self.WK.y:
							locations.remove(temp)
		if self.WR.y == self.WK.y:
			size = len(locations)
			for i in range(size):
				for temp in locations:
					if self.WR.x < self.WK.x:
						if temp[0]>self.WK.x:
							locations.remove(temp)
					else:
						if temp[0]<self.WK.x:
							locations.remove(temp)

		return locations



	def isCheck(self, player):
		if(player == "X"):
			if self.WK.getPos() in self.BK.getSurrounding():
				return True
		else:
			dangerZone = self.WK.getSurrounding()
			dangerZone.extend(rookway(self.WR))
			if self.BK.getPos() in dangerZone:
				return True
		return False

	def canCapture(self, player):
		if player == "X":
			kingway = self.WK.getSurrounding()
			if self.WR.capture == False:
				rway = rookway(self.WR)
			if (self.BK.x, self.BK.y) in kingway:
				return (True, "KING")
			if (self.BK.x, self.BK.y) in rway:
				return (True, "ROOK")
			return False
		else:
			kingway = self.BK.getSurrounding()
			if (self.WK.x, self.WK.y) in kingway:
				return (True, "KING")
			if self.WR.capture == False and (self.WR.x,self.WR.y) in kingway:
				return (True, "ROOK")
			return False

	def isCheckmate(self, player):
		if(player == "X"):
			# X player has only a King left
			if self.isCheck("X") and self.WR.capture == True:
				temp = self.availablePos(self.WK)
				dangerZone = self.BK.getSurrounding()
				for i in temp:
					if i in dangerZone:
						return True
				return False
		else:
			temp = self.availablePos(self.BK)
			if not temp:
				return True
			if self.WR.capture == False:
				dangerZone = self.WK.getSurrounding()
				dangerZone.extend(rookway(self.WR))
			else:
				dangerZone = self.WK.getSurrounding()
			for i in temp:
				if i in dangerZone:
					return True
			return False

	def inCorner(self, player):
		if player == "Y":
			if (self.BK.x,self.BK.y) == (0,0) and (self.WK.x,self.WK.y) in [(2,0),(2,1),(0,2),(1,2)]:
				return True
			if (self.BK.x,self.BK.y) == (0,7) and (self.WK.x,self.WK.y) in [(0,5),(1,5),(2,7),(2,6)]:
				return True
			if (self.BK.x,self.BK.y) == (7,0) and (self.WK.x,self.WK.y) in [(5,0),(5,1),(6,2),(7,2)]:
				return True
			if (self.BK.x,self.BK.y) == (7,7) and (self.WK.x,self.WK.y) in [(5,6),(5,7),(6,5),(7,5)]:
				return True
			return False

	def inCheckmatePos(self, player):
		if player == "Y":
			if self.BK.x == 0 and (self.WK.x,self.WK.y) == (self.BK.x +2,self.BK.y):
				return True
			if self.BK.y == 0 and (self.WK.x,self.WK.y) == (self.BK.x,self.BK.y + 2):
				return True
			if self.BK.x == 7 and (self.WK.x,self.WK.y) == (self.BK.x -2,self.BK.y):
				return True
			if self.BK.y == 7 and (self.WK.x,self.WK.y) == (self.BK.x,self.BK.y - 2):
				return True

	def inPreCheckmatePos(self, player):
		if player == "Y":
			if self.BK.y == 0:
				if (self.WK.x == (self.BK.x - 1) or self.WK.x == (self.BK.x +1)) and self.WK.y ==2:
					return True
			if self.BK.y == 7:
				if (self.WK.x == (self.BK.x - 1) or self.WK.x == (self.BK.x +1)) and self.WK.y ==5:
					return True
			if self.BK.x == 0:
				if (self.WK.y == (self.BK.y - 1) or self.WK.y == (self.BK.y +1)) and self.WK.x ==2:
					return True
			if self.BK.x == 7:
				if (self.WK.y == (self.BK.y - 1) or self.WK.y == (self.BK.y +1)) and self.WK.x ==5:
					return True
			return False

	def inFacingPos(self):
		if abs(self.WK.x - self.BK.x) == 2 and abs(self.BK.y - self.WK.y) <=1:# and self.WK.y in (self.BK.y,self.BK.y-1,self.BK.y+1):
			return True
		elif abs(self.WK.y - self.BK.y) == 2 and abs(self.WK.x - self.BK.x)<=1:# and self.WR.x in (self.BK.x,self.BK.x -1,self.BK.x +1):
			return True
		elif abs(self.WK.x - self.BK.x) == 2 and abs(self.WK.y - self.BK.y) == 2:
			return True
		else:
			return False

	def inEdge(self):
		if self.BK.x == 0 or self.BK.x == 7 or	self.BK.y ==0 or self.BK.y ==7:
			return True
		else:
			return False

	def isSpecialCheckmate(self):
		if self.BK.y == 0 or self.BK.y ==7:
			if self.WR.x in (self.BK.x+1,self.BK.x-1):
				return True
			else:
				return False
		else:
			if self.WR.y in (self.BK.y+1,self.BK.y-1):
				return True
			else:
				return False



	def move(self, ptype, y, x):
		if ptype == "WK":
			self.WK.updatePos(y,x)
		elif ptype == "WR":
			self.WR.updatePos(y,x)
		else:
			self.BK.updatePos(y,x)

		
def printBoard(xK,xR,yK):
    print("+----+----+----+----+----+----+----+----+")
    output.write("+----+----+----+----+----+----+----+----+\n")
    for i in range(0,8):
        for j in range(0,8):
            print("| ",end="")
            output.write("| " + "")
            if((i,j) == (xK.x,xK.y) and xK.capture == False):
                print("WK ",end="")
                output.write("WK " + "")
            elif ((i,j)== (xR.x,xR.y) and xR.capture == False):
                print("WR ",end="")
                output.write("WR " +"")
            elif((i,j) == (yK.x,yK.y) and yK.capture == False):
                print("BK ",end="")
                output.write("BK " +"")
            else:
                print("   ",end="")
                output.write("   " +"")
        print("|\n+----+----+----+----+----+----+----+----+")
        output.write("|\n+----+----+----+----+----+----+----+----+\n")



def heustric(board, currentTurn):
	blackScore = 0
	whiteScore = 0
	hvalue = 0
	dangerZone = []
	if currentTurn == "Y": # need to make it attack the rook
		if board.BK.x == 0 or board.BK.y == 0 or board.BK.x == 7 or board.BK.y == 7:
			hvalue -= 100000
		if board.BK.x == 1 or board.BK.y == 1 or board.BK.x == 6 or board.BK.y == 6:
			hvalue -= 200
		if board.BK.x == 2 or board.BK.y == 2 or board.BK.x == 5 or board.BK.y == 5:
			hvalue += 200
		if board.BK.x == 3 or board.BK.y == 3 or board.BK.x == 4 or board.BK.y == 4:
			hvalue += 10000
		dangerZone = board.WK.getSurrounding()
		if board.WR.capture == False:
			dangerZone.extend(board.availablePos(board.WR))
			# two lines below will make BK attack the rook
			# distance = math.sqrt(math.pow((board.WR.x - board.BK.x),2) + math.pow((board.WR.y - board.BK.y),2))
			# hvalue += (10 -distance)*10000
		if (board.BK.x,board.BK.y) in dangerZone:
			hvalue -=100000000

		if board.BK.x == 0 and board.WR.x == 1 and board.BK.y == board.WK.y:
			hvalue -= 10000000
		if board.BK.x == 7 and board.WR.x == 6 and board.BK.y == board.WK.y:
			hvalue -= 10000000
		if board.BK.y == 0 and board.WR.y == 1 and board.BK.x == board.WK.x:
			hvalue -= 10000000
		if board.BK.y == 7 and board.WR.y == 6 and board.BK.x == board.WK.x:
			hvalue -= 10000000
		if board.BK.y == 7 and board.WR.y == 6 and board.BK.x == board.WK.x and board.WR.x in (board.BK.x +1,board.BK.x-1):
			hvalue += 10000000

		return hvalue
	else: #player X
		if board.WR.capture == False:
			hvalue += 1000
		distance = math.sqrt(math.pow((board.WK.x - board.BK.x),2) + math.pow((board.WK.y - board.BK.y),2))
		hvalue -= distance*10000
		distance = math.sqrt(math.pow((board.WK.x - board.WR.x),2) + math.pow((board.WK.y - board.WR.y),2))
		hvalue -= distance*1000
		if(board.WR.x,board.WR.y) in board.BK.getSurrounding() and (board.WR.x,board.WR.y) not in board.WK.getSurrounding():
			hvalue -=100000000000
		if (board.WK.x,board.WK.y) in board.BK.getSurrounding():
			hvalue -=100000000000
		if (board.BK.x,board.BK.y) in [(3,3),(3,4),(4,3),(4,4)]:
			hvalue -= 300

		if board.BK.x in (0,7) or board.BK.y in (0,7):
			if board.WK.x == board.BK.x or board.WK.y == board.BK.y:
				hvalue += 1000000
		if board.BK.x ==0 and board.WR.x ==1:
			if board.WK.x ==2:
				hvalue += 100000
		if board.BK.x ==7 and board.WR.x ==6:
			if board.WK.x ==5:
				hvalue +=1000000
		if board.BK.y ==0 and board.WR.y ==1:
			if board.WK.y ==2:
				hvalue +=1000000
			# if board.WK.x < board.BK.x and board.WK.x<board.WR.x:
			# 	if board.WK.y ==1:
			# 		hvalue += 1000000
			# if board.WK.x > board.BK.x and board.WK.x > board.WR.x:
			# 	if board.WK.y==1:
			# 		hvalue += 1000000
			# if board.WK.y == 2:
			# 	hvalue += 10000
		if board.BK.y ==7 and board.WR.y ==6:
			if board.WK.y ==5:
				hvalue += 1000000


		return hvalue




#WHITE PLAYER CONTAINS TWO PIECE (X)
#BLACK PLAYER CONTAINS ONE PIECE (Y)
#Generate total moves for player
def generateMoves(board, player):
	moves = []
	if player == "X":
		moves.extend(board.availablePos(board.WK))
		#if board.WR.capture == False:
		#	moves.extend(board.availablePos(board.WR))
	else:
		moves.extend(board.availablePos(board.BK))
	return moves


#MiniMax with alphaBeta Pruning
#@param board current board that is in play 
#@param player used to determine which player to generate moves in Tree
#@param depth determine how many levels to traverse
#@param alpha used for AlphaBeta algorithm
#@param beta used for Alpha Beta algorithm
#@param maxPlayer bool value to determine whether to find maximum or minimum
#@param currentTurn, whose turn it is used to calculate score of that player in heuristic function
#@return returns the best position to move to in tuple structure of (<PieceType>, xPosition, yPosition)
def alphaBeta(board, player, depth, alpha, beta, maxPlayer, currentTurn):
    if depth == 0:
        return (None, heustric(board, currentTurn))
    elif maxPlayer == True:
        bestValue = float("-infinity")
        bestMove = None
        #generate moves basedo n player using board members
        for child in generateMoves(board, player):
            newBoard = copy.deepcopy(board)
            
            if player == "Y":
                newBoard.BK.updatePos(child[1], child[2])
                val = alphaBeta(newBoard, "X", depth-1, alpha, beta, False, currentTurn)
                #bestValue = max(bestValue, alphaBeta(newBoard, "Y", depth-1,  alpha, beta, False)[1])
            else:
                if child[0] == "WK":
                    newBoard.WK.updatePos(child[1], child[2])
                else:
                    newBoard.WR.updatePos(child[1], child[2])
                val = alphaBeta(newBoard, "X", depth-1, alpha, beta, False, currentTurn)
                #bestValue = max(bestValue, alphaBeta(newBoard, "X", depth-1,  alpha, beta, False)[1])
            
            if val[1] > bestValue:
                bestValue = val[1]
                alpha = bestValue
                #print(child)
                #print(val[1])
                bestMove = child
            if beta <= alpha:
                break
        return(bestMove, bestValue)
                

    else:
        bestValue = float("infinity")
        bestMove = None
        for child in generateMoves(board, player):
            newBoard = copy.deepcopy(board)
            
            if player == "Y":
                newBoard.BK.updatePos(child[1], child[2])
                val = alphaBeta(newBoard, "X", depth-1, alpha, beta, True, currentTurn)
            else:
                if child[0] == "WK":
                    newBoard.WK.updatePos(child[1], child[2])
                else:
                    newBoard.WR.updatePos(child[1], child[2])
                val = alphaBeta(newBoard, "Y", depth-1, alpha, beta, True, currentTurn)
            if val[1] < bestValue:
                bestValue = val[1]
                beta = val[1]
                bestMove = child
            if beta <= alpha:
                break
        return(bestMove, bestValue)


def Move(board, player, alpha, beta):
	temp = alphaBeta(board, player, 1, alpha, beta, True, player)
	if temp[0][0] == "BK":
		output.write("BK move to (" +str(temp[0][1]) +"," +str(temp[0][2]) +")\n")
		print("BK move to (",temp[0][1],",",temp[0][2],")")
		board.BK.updatePos(temp[0][1], temp[0][2])
	elif temp[0][0] == "WK":
		output.write("WK move to (" + str(temp[0][1]) + "," + str(temp[0][2]) + ")\n")
		print("WK move to (",temp[0][1],",",temp[0][2],")")
		board.WK.updatePos(temp[0][1], temp[0][2])
	else:
		output.write("WR move to (" + str(temp[0][1]) + "," + str(temp[0][2]) + ")\n")
		print("WR move to (",temp[0][1],",",temp[0][2],")")
		board.WR.updatePos(temp[0][1], temp[0][2])
	board.printState()
	

	

def PrintWR(board):
	output.write("WR move to (" + str(board.WR.x) + "," + str(board.WR.y) + ")\n")
	print("WR move to (",board.WR.x,",",board.WR.y,")")
	board.printState()

def HandleCheckmate(board):
	#print("handle checkmate")
	if board.BK.x == 0 or board.BK.x == 7:
		if ((board.BK.x,board.WR.y) not in board.BK.getSurrounding()):
			board.WR.updatePos(board.BK.x,board.WR.y)
			PrintWR(board)
		elif board.WR.y == board.BK.y+1 :
			if board.BK.x<4:
				board.WR.updatePos(board.BK.x+1,board.WR.y)
				PrintWR(board)
			else:
				board.WR.updatePos(board.BK.x -1,board.WR.y)
				PrintWR(board)
		else:
			Move(board,"X",alpha,beta)
	else: # BK.y == 0  or BK.y ==7
		if ((board.WR.x,board.WR.y) not in board.BK.getSurrounding()):
			board.WR.updatePos(board.WR.x,board.BK.y)
			PrintWR(board)
		elif board.WR.y == board.BK.y+1 : # rook in danger zone
			if board.BK.x<4:
				if (board.WR.x,board.WR.y) != (board.BK.x+1,board.WR.y):
					board.WR.updatePos(board.BK.x+1,board.WR.y)
					PrintWR(board)
				else:
					board.WR.updatePos(7,board.WR.y)
					PrintWR(board)

			else:
				board.WR.updatePos(board.BK.x -1,board.WR.y)
				PrintWR(board)
		else:
			Move(board,"X",alpha,beta)


def HandleCorner(board):
	#print("handle corner")
	if (board.BK.x,board.BK.y) == (0,0):
		if board.WK.y ==2:
			if board.WR.x != board.WK.x:
				board.WR.updatePos(board.WR.x,0)
		elif board.WK.x == 2:
			if board.WR.y != board.WK.y:
				board.WR.updatePos(0,board.WR.y)
	elif (board.BK.x,board.BK.y) == (7,0):
		if board.WK.y ==2:
			if board.WR.x != board.WK.x:
				board.WR.updatePos(board.WR.x,0)
		elif board.WK.x == 5:
			if board.WR.y != board.WK.y:
				board.WR.updatePos(7,board.WR.y)
	elif (board.BK.x,board.BK.y) == (0,7):
		if board.WK.y ==5:
			if board.WR.x != board.WK.x:
				board.WR.updatePos(board.WR.x,7)
		elif board.WK.x == 2:
			if board.WR.y != board.WK.y:
				board.WR.updatePos(0,board.WR.y)
	elif (board.BK.x,board.BK.y) == (7,7):
		if board.WK.y ==5:
			if board.WR.x != board.WK.x:
				board.WR.updatePos(board.WR.x,7)
		elif board.WK.x == 5:
			if board.WR.y != board.WK.y:
				board.WR.updatePos(7,board.WR.y)
	print("WR move to (",board.WR.x,",",board.WR.y,")")
	board.printState()

def HandleFacing(board):
	#print("handle facing")
	if (board.WR.x < board.WK.x and board.WR.x >board.BK.x) or (board.WR.x > board.WK.x and board.WR.x <board.BK.x):
		if board.WK.y == board.BK.y:
			if board.BK.y < 4:
				if (board.WR.x,board.WK.y+1) != (board.WR.x,board.WR.y):
					board.WR.updatePos(board.WR.x,board.WK.y+1)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
			else:
				if (board.WR.x,board.WK.y-1) != (board.WR.x,board.WR.y):
					board.WR.updatePos(board.WR.x,board.WK.y-1)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
		else:
			if (board.WR.x,board.WK.y) != (board.WR.x,board.WR.y):
				board.WR.updatePos(board.WR.x,board.WK.y)
				PrintWR(board)
			elif board.WK.y == board.WR.y:
				if board.WK.y<board.BK.y:
					board.WR.updatePos(board.WR.x,board.WR.y+1)
					PrintWR(board)
				else:
					board.WR.updatePos(board.WR.x,board.WR.y-1)
					PrintWR(board)
			else: 
				Move(board,"X", alpha,beta)
	elif (board.WR.y < board.WK.y and board.WR.y >board.BK.y) or (board.WR.y > board.WK.y and board.WR.y <board.BK.y):
		if board.WK.x == board.BK.x:
			if board.BK.x < 4:
				if (board.WK.x+1,board.WR.y) != (board.WR.x,board.WR.y):
					board.WR.updatePos(board.WK.x+1,board.WR.y)
					PrintWR(board)
				elif (board.WK.x+1,board.WR.y) == (board.WR.x,board.WR.y):
					board.WR.updatePos(board.WK.x,board.WR.y)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
			else:
				if (board.WK.x-1,board.WR.y) != (board.WR.x,board.WR.y):
					board.WR.updatePos(board.WK.x-1,board.WR.y)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
		else: # WK and BK not in the same line
			if (board.WK.x,board.WR.y) != (board.WR.x,board.WR.y):
				board.WR.updatePos(board.WK.x,board.WR.y)
				PrintWR(board)
			elif board.WK.x == board.WR.x:
				if board.WK.x<board.BK.x:
					board.WR.updatePos(board.WR.x+1,board.WR.y)
					PrintWR(board)
				else:
					board.WR.updatePos(board.WR.x-1,board.WR.y)
					PrintWR(board)
			else:
				Move(board,"X", alpha,beta)

	elif abs(board.BK.x-board.WK.x)==2:
		if board.BK.x<board.WK.x:
			if (board.WK.x-1,board.WR.y) in rookway(board.WR):
				if (board.WK.x-1,board.WR.y) != (board.WR.x,board.WR.y) and (board.WK.x-1,board.WR.y) not in board.BK.getSurrounding() :
					board.WR.updatePos(board.WK.x-1,board.WR.y)
					PrintWR(board)
				elif (board.WK.x-1,board.WR.y) != (board.WR.x,board.WR.y) and (board.WK.x-1,board.WR.y) in board.BK.getSurrounding() and (board.WK.x-1,board.WR.y) in board.WK.getSurrounding():
					board.WR.updatePos(board.WK.x-1,board.WR.y)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
			else:
				Move(board,"X", alpha,beta)
		else:
			if (board.WK.x+1,board.WR.y) in rookway(board.WR):
				if (board.WK.x+1,board.WR.y) != (board.WR.x,board.WR.y) and (board.WK.x+1,board.WR.y) not in board.BK.getSurrounding():
					board.WR.updatePos(board.WK.x+1,board.WR.y)
					PrintWR(board)
				elif (board.WK.x+1,board.WR.y) != (board.WR.x,board.WR.y) and (board.WK.x+1,board.WR.y) in board.BK.getSurrounding() and (board.WK.x+1, board.WR.y) in board.WK.getSurrounding():
					board.WR.updatePos(board.WK.x+1,board.WR.y)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)	
			else:
				Move(board,"X", alpha,beta)	

	elif (abs(board.BK.y -board.WK.y) ==2):
		if board.BK.y<board.WK.y:
			if (board.WR.x,board.WK.y-1) in rookway(board.WR):
				if (board.WR.x,board.WK.y -1) != (board.WR.x,board.WR.y) and (board.WR.x,board.WK.y -1) not in board.BK.getSurrounding():
					board.WR.updatePos(board.WR.x,board.WK.y -1)
					PrintWR(board)
				elif (board.WR.x,board.WK.y -1) != (board.WR.x,board.WR.y) and (board.WR.x,board.WK.y -1) in board.BK.getSurrounding() and (board.WR.x,board.WK.y -1) in board.WK.getSurrounding():
					board.WR.updatePos(board.WR.x,board.WK.y -1)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
			else:
				board.WR.updatePos(board.WR.x,board.BK.y+1)
				PrintWR(board)
		else: # BK on the right hand side of the rook
			if board.WR.y == board.WK.y+1:
				board.WR.updatePos(board.WK.x,board.WR.y)
				PrintWR(board)
			elif (board.WR.x,board.WK.y+1) in rookway(board.WR):
				if (board.WR.x,board.WK.y +1) != (board.WR.x,board.WR.y) and (board.WR.x,board.WK.y +1) not in board.BK.getSurrounding():
					board.WR.updatePos(board.WR.x,board.WK.y +1)
					PrintWR(board)
				elif (board.WR.x,board.WK.y +1) != (board.WR.x,board.WR.y) and (board.WR.x,board.WK.y +1) in board.BK.getSurrounding() and (board.WR.x,board.WK.y +1) in board.WK.getSurrounding():
					board.WR.updatePos(board.WR.x,board.WK.y +1)
					PrintWR(board)
				else:
					Move(board,"X", alpha,beta)
			else:
				board.WR.updatePos(board.WR.x,board.BK.y-1)
				PrintWR(board)
	

def HandleEdge(board):
	#print("handle edge")
	if board.BK.y == 0:
		if board.WR.y == 1:
			if (board.BK.x,board.BK.y)==(0,0) and (1,1) in board.WK.getSurrounding():
				board.WR.updatePos(1,1)
				PrintWR(board)
			elif (board.BK.x,board.BK.y) == (7,0) and (6,1) in board.WK.getSurrounding():
				board.WR.updatePos(6,1)
				PrintWR(board)
			elif (board.WR.x,board.WR.y) in board.BK.getSurrounding() and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())) :# and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())):# or board.WK.y!=0: #(board.WR.x-1,board.WR.y) in board.WR.getSurrounding() or (board.WR.x+1,board.WR.y) in board.WR.getSurrounding():
				if board.BK.x < 4:
					if board.WR.x !=7 and (7,1) in board.legalMove(board.WR):
						board.WR.updatePos(7,1)
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
				else:		
					if board.WR.x !=0 and (0,1) in board.legalMove(board.WR):
						board.WR.updatePos(0,1)	
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
			elif abs(board.WK.y - board.BK.y) ==2 and abs(board.WK.x-board.BK.x) == 1:
				HandleFacing(board)
			else:
				Move(board,"X", alpha,beta)
		elif (board.WR.x,1) in board.WK.getSurrounding() or (board.WR.x,1) not in board.BK.getSurrounding():
			board.WR.updatePos(board.WR.x,1)
			PrintWR(board)
		else:
			Move(board,"X", alpha,beta)
	elif board.BK.y == 7:
		if board.WR.y == 6:
			if (board.BK.x,board.BK.y) == (0,7) and (1,6) in board.WK.getSurrounding():
				board.WR.updatePos(1,6)
				PrintWR(board)
			elif (board.BK.x,board.BK.y) == (7,7) and (6,6) in board.WK.getSurrounding():
				board.WR.updatePos(6,6)
				PrintWR(board)
			elif (board.WR.x,board.WR.y) in board.BK.getSurrounding() and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())) :# and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())):# or board.WK.y!=7: #(board.WR.x-1,board.WR.y) in board.WR.getSurrounding() or (board.WR.x+1,board.WR.y) in board.WR.getSurrounding():
				if board.BK.x < 4:
					if board.WR.x !=7 and (7,6) in board.legalMove(board.WR):
						board.WR.updatePos(7,6)	
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
				else:		
					if board.WR.x !=0 and (0,6) in board.legalMove(board.WR):
						board.WR.updatePos(0,6)	
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
			elif abs(board.WK.y - board.BK.y) ==2 and abs(board.WK.x-board.BK.x) == 1:
				HandleFacing(board)
			else:
				Move(board,"X", alpha,beta)
		elif board.WR.y !=6:
			if (board.WR.x,6) in board.WK.getSurrounding() or (board.WR.x,6) not in board.BK.getSurrounding():
				board.WR.updatePos(board.WR.x,6)
				PrintWR(board)
			else:
				Move(board,"X", alpha,beta)
	elif board.BK.x ==0:
		if board.WR.x ==1:
			if (board.WR.x, board.WR.y) in board.BK.getSurrounding() and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())):# or board.WK.x!=0: #(board.WR.x,board.WR.y+1) in board.WR.getSurrounding() or (board.WR.x,board.WR.y-1) in board.WR.getSurrounding():
				if board.BK.y <4:
					if board.WR.y !=7 and (1,7) in board.legalMove(board.WR):
						board.WR.updatePos(1,7)
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
				else:
					if board.WR.y !=0 and (1,0) in board.legalMove(board.WR):
						board.WR.updatePos(1,0)
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
			elif abs(board.WK.y - board.BK.y) ==1 and abs(board.WK.x-board.BK.x) == 2:
				HandleFacing(board)
			else:
				Move(board,"X", alpha,beta)
		elif board.WR.x !=1:
			if (1,board.WR.y) in board.WK.getSurrounding() or (1,board.WR.y) not in board.BK.getSurrounding():
				board.WR.updatePos(1,board.WR.y)
				PrintWR(board)
			else:
				Move(board,"X", alpha,beta)
	else:
		if board.WR.x ==6:
			if (board.WR.x, board.WR.y) in board.BK.getSurrounding() and not bool(set(board.WR.getSurrounding())&set(board.WK.getSurrounding())):# or board.WK.x!=7: #(board.WR.x, board.WR.y+1) in board.WR.getSurrounding() or (board.WR.x, board.WR.y-1) in board.WR.getSurrounding():
				if board.BK.y <4:
					if board.WR.y !=7 and (6,7) in board.legalMove(board.WR):
						board.WR.updatePos(6,7)
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
				else:
					if board.WR.y !=0 and (6,0) in board.legalMove(board.WR):
						board.WR.updatePos(6,0)
						PrintWR(board)
					else:
						Move(board,"X", alpha,beta)
			elif abs(board.WK.y - board.BK.y) ==1 and abs(board.WK.x-board.BK.x) == 2:
				HandleFacing(board)
			else:
				Move(board,"X", alpha,beta)
		elif board.WR.x !=6:
			if (6,board.WR.y) in board.WK.getSurrounding() or (6,board.WR.y) not in board.BK.getSurrounding():
				board.WR.updatePos(6,board.WR.y)
				PrintWR(board)
			else:
				Move(board,"X", alpha,beta)


def HandleUnderAttack(board):
	#print("handle under attacked")
	if (board.WR.x, board.WR.y) in board.WK.getSurrounding():
		Move(board,"X", alpha,beta)
	elif board.BK.x >3 and (board.WR.x -2,board.WR.y) in board.WK.getSurrounding():
		board.WR.updatePos(board.WR.x -2,board.WR.y)
	elif board.BK.x < 4 and (board.WR.x +2,board.WR.y) in board.WK.getSurrounding():
		board.WR.updatePos(board.WR.x +2,board.WR.y)

	elif board.BK.x == 0 and board.WR.x==1:
		if board.WR.y <=3:
			board.WR.updatePos(board.WR.x,7)
		else:
			board.WR.updatePos(board.WR.x,0)
	elif board.BK.x == 7 and board.WR.x == 6:
		if board.WR.y <=3:
			board.WR.updatePos(board.WR.x,7)
		else:
			board.WR.updatePos(board.WR.x,0)
	elif board.BK.y == 0 and board.WR.y == 1:
		if board.WR.x <=3:
			board.WR.updatePos(7,board.WR.y)
		else:
			board.WR.updatePos(0,board.WR.y)
	elif board.BK.y ==7 and board.WR.y ==6:
		if board.WR.y <=3:
			board.WR.updatePos(board.WR.x,7)
		else:
			board.WR.updatePos(board.WR.x,0)
	else:
		if board.BK.x < board.BK.y:
			if board.BK.x<4:
				board.WR.updatePos(7,board.WR.y)
			else:
				board.WR.updatePos(0,board.WR.y)
		else:
			if board.BK.y<4:
				board.WR.updatePos(board.WR.x,7)
			else:
				board.WR.updatePos(board.WR.x,0)
	PrintWR(board)

def HandlePreCheckmate(board):
	#print("handle pre-checkmate")
	if board.BK.x == 0 or board.BK.x == 7:
		if board.WR.x == 1 or board.WR.x ==6:
			#if (board.WR.x,board.WR.y) in board.WK.getSurrounding():
			#	Move(board,"X",alpha,beta)
			#else:
			Move(board,"X",alpha,beta)

		elif board.WR.y != board.BK.y -1 and board.WR.y != board.BK.y +1 and board.WR.y != board.WK.y:
			if board.BK.x == 0:
				board.WR.updatePos(board.BK.x+1,board.WR.y)
			else:
				board.WR.updatePos(board.BK.x -1, board.WR.y)
			PrintWR(board)
		else:
			Move(board,"X",alpha,beta)
	elif board.BK.y == 0 or board.BK.y == 7:
		if board.WR.y == 1 or board.WR.y ==6:
			Move(board,"X", alpha,beta)
		elif board.WR.x != board.BK.x - 1 and board.WR.x != board.BK.x +1 and board.WR.x != board.WK.x:
			if board.BK.y ==0:
				board.WR.updatePos(board.WR.x,board.BK.y+1)
			else:
				board.WR.updatePos(board.WR.x,board.BK.y-1)
			PrintWR(board)
		else:
			Move(board,"X",alpha,beta)


def Play(moves, board):
	i = 0
	while i<moves:
		# Y move first
		if board.isCheckmate("Y"):
			output.write("X win, Checkmate\n")
			board.BK.capture == True
			print("X win, Checkmate")
			break
		else:
			output.write("\nMove #" + str(i+1) +"\n")
			print("\nMove #",i+1)
			output.write("Y turn\n")
			print("Y turn")
			temp = board.canCapture("Y")
			if temp!= False:
				if temp[1] == "KING":
					board.BK.updatePos(board.WK.x,board.WK.y)
					board.WK.capture = True
					board.printState()
					output.write("Y win\n")
					print("Y win")
					break
				else:
					if (board.WR.x, board.WR.y) not in board.WK.getSurrounding(): 
						board.BK.updatePos(board.WR.x, board.WR.y)
						board.WR.capture = True
						board.printState()
						output.write("Draw!\n")
						print("Draw!")
						break
			Move(board,"Y", alpha, beta)
		
		# X move
		if board.isCheckmate("X"): # almost never happen
			output.wrte("Y win, Checkmate\n")
			print("Y win, Checkmate")
			break
		if board.WR.capture == True:
			board.printState()
			output.write("Draw!\n")
			print("Draw!")
			break
		else:
			output.write("\nX turn\n")
			print("\nX turn")
			if (board.BK.x, board.BK.y) in board.WK.getSurrounding():
				board.BK.capture == True
				board.WK.updatePos(board.BK.x, board.BK.y)
				board.printState()
				output.write("X win\n")
				print("X win")
				break
			elif (board.BK.x, board.BK.y) in board.availablePos(board.WR):
				board.BK.capture == True
				board.WR.updatePos(board.BK.x, board.BK.y)
				board.printState()
				output.write("X win\n")
				print("X win")
				break
			# handle corner
			elif board.inCorner("Y"):
				HandleCorner(board)
			
			#handle checkmate Position
			elif board.inCheckmatePos("Y") and not board.isSpecialCheckmate():
				HandleCheckmate(board)

			# BK in the edge
			elif board.inEdge():
				HandleEdge(board)
				
			#handle pre-checkmate position
			elif board.inPreCheckmatePos("Y"):
				HandlePreCheckmate(board)
										
			#handle facing case
			elif board.inFacingPos():
				HandleFacing(board)

			# if WR is attacked 
			elif (board.WR.x, board.WR.y) in board.BK.getSurrounding() :
				HandleUnderAttack(board)		

			# use alphaBeta to pick a best move
			else:
				output.write("handle normal case\n")
				print("handle normal case")
				Move(board,"X", alpha, beta)

		i += 1
	if i ==35:
		output.write("Draw!\n")
		print("Draw!")
		output.write("Number of moves made: " + str(i) + "\n")
		print("Number of moves made: ", i)
	else:
		output.write("Number of moves made: " + str(i) + "\n")
		print("Number of moves made: ", i)

def PlayX(board):
	if board.isCheckmate("X"): # almost never happen
			print("Y win, Checkmate")
	if board.WR.capture == True:
		board.printState()
		print("Draw!")
	else:
		output.write("\nX turn\n")
		print("\nX turn")
		if (board.BK.x, board.BK.y) in board.WK.getSurrounding():
			board.BK.capture == True
			board.WK.updatePos(board.BK.x, board.BK.y)
			board.printState()
			print("X win")
		elif (board.BK.x, board.BK.y) in board.availablePos(board.WR):
			board.BK.capture == True
			board.WR.updatePos(board.BK.x, board.BK.y)
			board.printState()
			print("X win")
		# handle corner
		elif board.inCorner("Y"):
			HandleCorner(board)
		
		#handle checkmate Position
		elif board.inCheckmatePos("Y") and not board.isSpecialCheckmate():
			HandleCheckmate(board)

		# BK in the edge
		elif board.inEdge():
			HandleEdge(board)
			
		#handle pre-checkmate position
		elif board.inPreCheckmatePos("Y"):
			HandlePreCheckmate(board)
									
		#handle facing case
		elif board.inFacingPos():
			HandleFacing(board)

		# if WR is attacked 
		elif (board.WR.x, board.WR.y) in board.BK.getSurrounding() :
			HandleUnderAttack(board)		

		# use alphaBeta to pick a best move
		else:
			output.write("handle normal case\n")
			print("handle normal case")
			Move(board,"X", alpha, beta)


def PlayY(board):
	if board.isCheckmate("Y"):
			board.BK.capture == True
			print("X win, Checkmate")
	else:
		output.write("\nMove #" + str(i+1) +"\n")
		print("\nMove #",i+1)
		print("Y turn")
		temp = board.canCapture("Y")
		if temp!= False:
			if temp[1] == "KING":
				board.BK.updatePos(board.WK.x,board.WK.y)
				board.WK.capture = True
				board.printState()
				print("Y win")
			else:
				if (board.WR.x, board.WR.y) not in board.WK.getSurrounding(): 
					board.BK.updatePos(board.WR.x, board.WR.y)
					board.WR.capture = True
					board.printState()
					print("Draw!")
		Move(board,"Y", alpha, beta)

def main():
	
	temp = Board()
	listPieces = read(fileRead)
	
	command = input("Enter a command: (Play) ")
	if command == "Play":
		test = input("Is this a test?: Y/N ")
		if test == "Y":
			numMoves = input("Enter maximum number of moves: (default is 35) ")
			
			for x in range(0,3):
				temp.addPiece(listPieces[x][0], listPieces[x][1], listPieces[x][3], listPieces[x][2])
				#temp.addPiece(x[0], x[1], x[3], x[2])
			output.write("Game Started\n")
			print("Game Started")
			output.write("Testcase1: ")
			print("Testcase1: ", end="")
			for x in range(0,3):
				output.write(str(listPieces[x]))
				print(listPieces[x], end = "")

			output.write("\nInitial board\n")
			print("\nInitial board")
			temp.printState()
			Play(int(numMoves), temp)


			temp = Board()

			for x in range(3,6):
				temp.addPiece(listPieces[x][0], listPieces[x][1], listPieces[x][3], listPieces[x][2])
			output.write("\nGame Started\n")
			print("\nGame Started")
			output.write("Testcase2: ")
			print("Testcase2: ", end="")
			for x in range(0,3):
				output.write(str(listPieces[x]))
				print(listPieces[x], end = "")

			output.write("\nInitial board\n")
			print("\nInitial board")
			temp.printState()
			Play(int(numMoves), temp)


		else:
			print("GoodBye!")	
	else:
		print("Starting Champion Game!")
	output.close()	



temp = Board()
# take 14
# temp.addPiece("X","WR",7,1)
# temp.addPiece("X","WK",4,4)
# temp.addPiece("Y","BK",2,2)

# take 20 moves or 14
# temp.addPiece("X","WR",4,5)
# temp.addPiece("X","WK",4,4)
# temp.addPiece("Y","BK",2,2)

# 4 moves
# temp.addPiece("X","WR",1,4)
# temp.addPiece("X","WK",0,6)
# temp.addPiece("Y","BK",0,0)


# temp.addPiece("X","WR",4,5)
# temp.addPiece("X","WK",7,4)
# temp.addPiece("Y","BK",1,2)


# take 6 moves
# temp.addPiece("X","WR",4,1)
# temp.addPiece("X","WK",1,2)
# temp.addPiece("Y","BK",1,0)

#take 4 moves
# temp.addPiece("X","WR",7,5)
# temp.addPiece("X","WK",4,5)
# temp.addPiece("Y","BK",5,7)


#take 12 moves
# temp.addPiece("X","WR",5,6)
# temp.addPiece("X","WK",6,5)
# temp.addPiece("Y","BK",4,7)

#testcase 1
# temp.addPiece("X","WR",7,4)
# temp.addPiece("X","WK",4,5)
# temp.addPiece("Y","BK",5,7)

#testcase 2
# temp.addPiece("X","WR",4,5)
# temp.addPiece("X","WK",5,4)
# temp.addPiece("Y","BK",3,6)


temp.addPiece("X","WR",4,6)
temp.addPiece("X","WK",4,5)
temp.addPiece("Y","BK",5,7)



#temp.printState()
# PlayX(temp)

Play(35,temp)




def PlayerX():
	i = 0
	while i<35:
		wk = input("Enter white king position ")
		temp.addPiece("X","WK",int(wk[0]),int(wk[2]))
		wr = input("Enter white rook position ")
		temp.addPiece("X","WR",int(wr[0]),int(wr[2]))
		bk = input("Enter black king position ")
		temp.addPiece("Y","BK",int(bk[0]),int(bk[2]))
		temp.printState()
		PlayX(temp)
		i +=1

def PlayerY():
	i = 0
	while i<35:
		wk = input("Enter white king position ")
		temp.addPiece("X","WK",int(wk[0]),int(wk[2]))
		wr = input("Enter white rook position ")
		temp.addPiece("X","WR",int(wr[0]),int(wr[2]))
		bk = input("Enter black king position ")
		temp.addPiece("Y","BK",int(bk[0]),int(bk[2]))
		temp.printState()
		PlayX(temp)
		i +=1

# PlayerX()

# pause screen
import msvcrt as m
def wait():
    m.getch()
wait()

