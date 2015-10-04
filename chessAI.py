import math	
import copy
		
#http://chessprogramming.wikispaces.com/Simplified+evaluation+function
#Piece Values for chess piece
Rook = 500
King = 20000

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
	return locations

class Board:
	def __init__(self):
		self.WK = Piece()
		self.WR = Piece()
		self.BK = Piece()

	def addPiece(self,player,ptype,x,y):
		if(player == "X"):
			if(ptype == "KING"):
				self.WK.setValue(player,ptype,x,y)
			else:
				self.WR.setValue(player,ptype,x,y)
		else:
			self.BK.setValue(player,ptype,x,y)

	def printState(self):
		printBoard(self.WK,self.WR, self.BK)

	def availablePos(self,piece):
		available = []
		if(piece.player == "X"):
			dangerZone = self.BK.getSurrounding()
			if(piece.ptype == "KING"):
				available = piece.getSurrounding()
			else:
				available = rookway(piece)
		else:
			available = piece.getSurrounding()
			dangerZone = rookway(self.WR) + self.WK.getSurrounding()
		for temp in available:
					if temp in dangerZone:
						available.remove(temp)
		return available

	def legalMove(self, piece):
		current = (piece.x,piece.y)
		if(piece.player == "X"):
			dangerZone = self.BK.getSurrounding()
			if(piece.ptype == "KING"):
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

		
def printBoard(xK,xR,yK):
    print("+----+----+----+----+----+----+----+----+")
    for i in range(0,8):
        for j in range(0,8):
            print("| ",end="")
            if((i,j) == (xK.x,xK.y)):
                print("WK ",end="")
            elif ((i,j)== (xR.x,xR.y)):
                print("WR ",end="")
            elif((i,j) == (yK.x,yK.y)):
                print("BK ",end="")
            else:
                print("   ",end="")
        print("|\n+----+----+----+----+----+----+----+----+")



def heustric(board, player):
	blackScore = 0
	whiteScore = 0

	if board.BK.capture == False:
		whiteScore += King
		whiteScore += pieceSquareTableKing[abs((board.BK.y)-7)][board.BK.x]

	if board.WK.capture == False:
		blackScore += King
		blackScore += pieceSquareTableKing[board.WK.y][board.WK.x]

	if board.WR.capture == False:
		blackScore += Rook
		blackScore += pieceSquareTableRook[board.WR.y][board.WR.x]	

	if (player == "X"):
		return blackScore - whiteScore
	else:
		return whiteScore - blackScore	



#BLACK PLAYER CONTAINS ONE PIECE (X)
#WHITE PLAYER CONTAINS TWO PIECE (Y)
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


#MiniMax function with no Pruning
def search(board, player, depth, maxPlayer):
	if depth == 0: 
		#print((None, heustric(board, player)))
		return (None, heustric(board, player))
	elif maxPlayer == True:
		bestValue = float('-infinity')
		bestMove = None

		#generate moves based on player
		for child in generateMoves(board, player):
			newBoard = copy.deepcopy(board)
			#newBoard = board
			if player == "X":
				newBoard.BK.updatePos(child[0],child[1])
				val = search(newBoard,"Y", depth-1, False)	
			else:
				if child[0] == "WK":
					newBoard.WK.updatePos(child[0],child[1])
				else:
					newBoard.WR.updatePos(child[0],child[1])	
				val = search(newBoard,"X", depth-1, False)
			if val[1] > bestValue:
				bestValue = val[1]
				bestMove = child
		#print (bestMove, bestValue)			
		return (bestMove, bestValue)

	else:
		bestValue = float('infinity')
		bestMove = None

		for child in generateMoves(board, player):
			newBoard = copy.deepcopy(board)
			#newBoard = board
			if player == "X":
				newBoard.BK.updatePos(child[0],child[1])
				val = search(newBoard,"Y", depth-1, True)	
			else: 
				if child[0] == "WK":
					newBoard.WK.updatePos(child[0],child[1])
				else:
					newBoard.WR.updatePos(child[0],child[1])	
				val = search(newBoard,"X", depth-1, True)
			if val[1] < bestValue:
				bestValue = val[1]
				bestMove = child
		print (bestMove, bestValue)		
		return (bestMove, bestValue)





temp = Board()
temp.addPiece("X","ROOK",0,1)
temp.addPiece("X","KING",0,5)
temp.addPiece("Y","KING",1,5)
temp.printState()

pos = generateMoves(temp,"X")
print(pos)
print(temp.isCheck("X"))

print(search(temp, "X",2,True))
