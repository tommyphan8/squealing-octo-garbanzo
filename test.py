import math	
import copy
import time


alpha = float("-infinity")
beta = float("infinity")


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
		print(self.player,self.ptype,"(",self.x,",",self.y,")")

	def getSurrounding(self):
		temp= [(self.x+1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1), (self.x, self.y+1), (self.x, self.y-1), (self.x+1, self.y), (self.x-1, self.y)]
		temp = [x for x in temp if x[0]>=0 and x[0]<=7]
		temp = [x for x in temp if x[1]>=0 and x[1]<=7]
		return temp

def rookway(piece):
	locations = []
	for i in range(0,8):
		locations.append((i, piece.y))
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
		if piece.player == "X":
			dangerZone = self.BK.getSurrounding()
			if piece.ptype == "WK":
				available = self.WK.getSurrounding()
			elif piece.ptype == "WR" and piece.capture == False:
				available = rookway(piece)
		elif piece.ptype == "BK":
			available = self.BK.getSurrounding()
			dangerZone = self.WK.getSurrounding()
			if self.WR.capture == False:
				dangerZone.extend(rookway(self.WR))

		size = len(available)
		for i in range(size):
			for temp in available:
				if temp in dangerZone:
					available.remove(temp) 

		for i in available:
			result.append((piece.ptype, i[0], i[1]))
		return result



	def legalMove(self, piece):
		current = (piece.x,piece.y)
		if(piece.player == "X"):
			dangerZone = self.BK.getSurrounding()
			if(piece.ptype == "WK"):
				if ((self.WR.x, self.WR.y) in dangerZone):
					return False
				else: 
					return True
			else:
				if((self.WK.x, self.WK.y) in dangerZone):
					return False
				else:
					return True

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

	def move(self, ptype, y, x):
		if ptype == "WK":
			self.WK.updatePos(y,x)
		elif ptype == "WR":
			self.WR.updatePos(y,x)
		else:
			self.BK.updatePos(y,x)

		
def printBoard(xK,xR,yK):
    print("+----+----+----+----+----+----+----+----+")
    for i in range(0,8):
        for j in range(0,8):
            print("| ",end="")
            if((i,j) == (xK.x,xK.y) and xK.capture == False):
                print("WK ",end="")
            elif ((i,j)== (xR.x,xR.y) and xR.capture == False):
                print("WR ",end="")
            elif((i,j) == (yK.x,yK.y) and yK.capture == False):
                print("BK ",end="")
            else:
                print("   ",end="")
        print("|\n+----+----+----+----+----+----+----+----+")



def heustric(board, currentTurn):
	blackScore = 0
	whiteScore = 0
	hvalue = 0
	dangerZone = []
	if currentTurn == "Y": # need to make it attack the rook
		if board.BK.x == 0 or board.BK.y == 0 or board.BK.x == 7 or board.BK.y == 7:
			hvalue -= 1000
		if board.BK.x == 1 or board.BK.y == 1 or board.BK.x == 6 or board.BK.y == 6:
			hvalue -= 800
		if board.BK.x == 2 or board.BK.y == 2 or board.BK.x == 5 or board.BK.y == 5:
			hvalue += 200
		if board.BK.x == 3 or board.BK.y == 3 or board.BK.x == 4 or board.BK.y == 4:
			hvalue += 1000
		dangerZone = board.WK.getSurrounding()
		if board.WR.capture == False:
			dangerZone.extend(rookway(board.WR))
			# two lines below will make BK attack the rook
			distance = math.sqrt(math.pow((board.WR.x - board.BK.x),2) + math.pow((board.WR.y - board.BK.y),2))
		hvalue += (10 -distance)*10000
		if (board.BK.x,board.BK.y) in dangerZone:
			hvalue -=100000000

		return hvalue
	else: #player X
		if board.WR.capture == False:
			hvalue += 100
		distance = math.sqrt(math.pow((board.WK.x - board.BK.x),2) + math.pow((board.WK.y - board.BK.y),2))
		hvalue -= distance*100

		return hvalue




#WHITE PLAYER CONTAINS TWO PIECE (X)
#BLACK PLAYER CONTAINS ONE PIECE (Y)
#Generate total moves for player
def generateMoves(board, player):
	moves = []
	if player == "X":
		moves.extend(board.availablePos(board.WK))
		if board.WR.capture == False:
			moves.extend(board.availablePos(board.WR))
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
		print("BK move to (",temp[0][1] + 1,",",temp[0][2] +1,")")
		board.BK.updatePos(temp[0][1], temp[0][2])
	elif temp[0][0] == "WK":
		print("WK move to (",temp[0][1] + 1,",",temp[0][2] +1,")")
		board.WK.updatePos(temp[0][1], temp[0][2])
	else:
		print("WR move to (",temp[0][1] + 1,",",temp[0][2] +1,")")
		board.WR.updatePos(temp[0][1], temp[0][2])
	board.printState()
	


def Play(moves, board):
	i = 0
	while i<moves:
		# Y move first
		if board.isCheckmate("Y"):
			print("X win, Checkmate")
			break
		else:
			print("\nY turn")
			temp = board.canCapture("Y")
			if temp!= False:
				if temp[1] == "KING":
					board.BK.updatePos(board.WK.x,board.WK.y)
					board.WK.capture = True
					board.printState()
					print("Y win")
					break
				else:
					if (board.WR.x, board.WR.y) not in board.WK.getSurrounding(): 
						board.BK.updatePos(board.WR.x, board.WR.y)
						board.WR.capture = True
						board.printState()
						print("Draw!")
						break
			Move(board,"Y", alpha, beta)
		
		# X move
		if board.isCheckmate("X"): # almost never happen
			print("Y win, Checkmate")
			break
		if board.WR.capture == True:
			board.printState()
			print("Draw!")
			break
		else:
			print("\nX turn")
			if (board.BK.x, board.BK.y) in board.WK.getSurrounding():
				board.BK.capture == True
				board.WK.updatePos(board.BK.x, board.BK.y)
				board.printState()
				print("X win")
				break
			elif (board.BK.x, board.BK.y) in rookway(board.WR):
				board.BK.capture == True
				board.WR.updatePos(board.BK.x, board.BK.y)
				board.printState()
				print("X win")
				break
			# handle corner
			elif board.inCorner("Y"):
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
			# handle checkmate position
			elif board.inCheckmatePos("Y"):
				if (board.WK.x,board.WK.y) not in rookway(board.WR):
					if board.BK.x == 0 or board.BK.x == 7:
						board.WR.updatePos(board.BK.x,board.WR.y)
						print("WR move to (",board.WR.x,",",board.WR.y,")")
						board.printState()
					else:
						board.WR.updatePos(board.WR.x,board.BK.y)
						print("WR move to (",board.WR.x,",",board.WR.y,")")
						board.printState()

			# if WR is attacked 
			elif (board.WR.x, board.WR.y) in board.BK.getSurrounding():
				if(board.WR.x <=3):
					board.WR.updatePos(7,board.WR.y)
					print("WR move to (",board.WR.x,",",board.WR.y,")")
					board.printState()
				elif board.WR.x >=4:
					board.WR.updatePos(0,board.WR.y)
					print("WR move to (",board.WR.x,",",board.WR.y,")")
					board.printState()
			else:
				Move(board,"X", alpha, beta)

		i += 1


def testCase(board, alpha, beta):
    temp = None
    temp1 = None
    for x in range (1,2, 1):
        print("\nDepth: ", x)
        startTime = time.clock()
        temp = alphaBeta(board, "X", x, alpha, beta, True, "X")
        print(temp)
        print("AlphaBeta", time.clock() - startTime, "seconds")



temp = Board()
temp.addPiece("X","WR",7,1)
temp.addPiece("X","WK",0,3)
temp.addPiece("Y","BK",7,5)
print("initial board")
temp.printState()


print(temp.availablePos(temp.WK))




Play(35, temp)






# pause screen
import msvcrt as m
def wait():
    m.getch()
wait()

