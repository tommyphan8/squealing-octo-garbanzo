import math	
import copy
import time

#http://chessprogramming.wikispaces.com/Simplified+evaluation+function
#Piece Values for chess piece
Rook = 500
King = 20000

alpha = float("-infinity")
beta = float("infinity")

#Piece-Square Tables 
pieceSquareTableKing = [[] for i in range(8)]
pieceSquareTableRook = [[] for i in range(8)]

pieceSquareTableKing[0] = [-50,-40,-30,-20,-20,-30,-40,-50]
pieceSquareTableKing[1] = [-30,-20,-10,  0,  0,-10,-20,-30]
pieceSquareTableKing[2] = [-30,-10, 20, 30, 30, 20,-10,-30]
pieceSquareTableKing[3] = [-30,-10, 30, 40, 40, 30,-10,-30]
pieceSquareTableKing[4] = [-30,-10, 30, 40, 40, 30,-10,-30]
pieceSquareTableKing[5] = [-30,-10, 20, 30, 30, 20,-10,-30]
pieceSquareTableKing[6] = [-30,-30,  0,  0,  0,  0,-30,-30]
pieceSquareTableKing[7] = [-50,-30,-30,-30,-30,-30,-30,-50]

pieceSquareTableRook[0] = [0,  0,  0,  0,  0,  0,  0,  0]
pieceSquareTableRook[1] = [5, 10, 10, 10, 10, 10, 10,  5]
pieceSquareTableRook[2] = [-5,  0,  0,  0,  0,  0,  0, -5]
pieceSquareTableRook[3] = [-5,  0,  0,  0,  0,  0,  0, -5]
pieceSquareTableRook[4] = [-5,  0,  0,  0,  0,  0,  0, -5]
pieceSquareTableRook[5] = [-5,  0,  0,  0,  0,  0,  0, -5]
pieceSquareTableRook[6] = [-5,  0,  0,  0,  0,  0,  0, -5]
pieceSquareTableRook[7] = [0,  0,  0,  5,  5,  0,  0,  0]

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

	locations = [x for x in moves if x != (piece.x,piece.y)]
    locations = [x for x in moves if x != (piece.x,piece.y)]
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
		if(piece.player == "X"):
			dangerZone = self.BK.getSurrounding()
			if(piece.ptype == "WK"):
				available = piece.getSurrounding()				
			else:
				available = rookway(piece)
			for i in available:
				result.append((piece.ptype, i[0], i[1]))
		else:
			available = piece.getSurrounding()
			for i in available:
				result.append((piece.ptype, i[0], i[1]))
			dangerZone = self.WK.getSurrounding()
			dangerZone.extend(rookway(self.WR))
		for temp in result:
			if (temp[1],temp[2]) in dangerZone:
				result.remove(temp)
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
			if self.WR.capture == True:
				dangerZone = self.WK.getSurrounding()
			else:
				dangerZone = self.WK.getSurrounding()
				dangerZone.extend(rookway(self.WR))
			for i in temp:
				if i in dangerZone:
					return True
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

	if board.BK.capture == False:
		blackScore += King
		blackScore += pieceSquareTableKing[abs((board.BK.x)-7)][board.BK.y]

	if board.WK.capture == False:
		whiteScore += King
		whiteScore += pieceSquareTableKing[board.WK.x][board.WK.y]

	if board.WR.capture == False:
		whiteScore += Rook
		whiteScore += pieceSquareTableRook[board.WR.x][board.WR.y]	

	if (currentTurn == "Y"):
		return blackScore - whiteScore
	else:
		return whiteScore - blackScore	


def heuristicX(board, piece, pos):
	blackScore = 0
	whiteScore = 0


	


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
	temp = alphaBeta(board, player, 5, alpha, beta, True, player)
	if temp[0][0] == "BK":
		#print("Y move")
		board.BK.updatePos(temp[0][1], temp[0][2])
	elif temp[0][0] == "WK":
		#print("X move")
		board.WK.updatePos(temp[0][1], temp[0][2])
	else:
		#print("X move")
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
			print("Y move")
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
			print("X move")
			if (board.BK.x, board.BK.y) in board.WK.getSurrounding():
				board.BK.capture == True
				board.WK.updatePos(board.BK.x, board.BK.y)
				board.printState()
				print("X win")
				break
			if (board.BK.x, board.BK.y) in rookway(board.WR):
				board.BK.capture == True
				board.WR.updatePos(board.BK.x, board.BK.y)
				board.printState()
				print("X win")
				break


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
temp.addPiece("X","WR",6,1)
temp.addPiece("X","WK",1,5)
temp.addPiece("Y","BK",1,3)
print("initial board")
temp.printState()

print("rook way")
print(rookway(temp.WR))
print("availablePos")
print(temp.availablePos(temp.BK))

Play(35, temp)






# pause screen
import msvcrt as m
def wait():
    m.getch()
wait()

