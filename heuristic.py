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

	def updatePos(self, x, y):
		self.x = x
		self.y = y	


class Board:
    def __init__(self):
        self.WK = Piece()
        self.WR = Piece()
        self.BK = Piece()

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


                        
#Generate PSEUDO MOVES WILL NEED TO BE FILTERED TO LEGAL MOVES
def genMovesKing(p):
	moves = []
	moves.extend(((p.ptype,p.x-1, p.y), (p.ptype,p.x+1,p.y), (p.ptype,p.x,p.y+1), (p.ptype,p.x-1,p.y+1), (p.ptype,p.x+1, p.y+1), (p.ptype,p.x, p.y-1), (p.ptype,p.x+1, p.y-1), (p.ptype,p.x-1, p.y-1)))
	
	#filter out pieces that are out the boundary
	moves = [x for x in moves if x[1] >= 0 and x[1] <= 7 ]
	moves = [x for x in moves if x[2] >= 0 and x[2] <= 7]
			
	return moves

#Generate possible moves for input:piece
def genMovesRook(p):
	moves = []
	for i in range(0,8):
		moves.append((p.ptype,p.x,i))

	for i in range(0,8):
		moves.append((p.ptype,i,p.y))

	#filter out duplicated self piece
	moves = [x for x in moves if x != (p.ptype,p.x,p.y)]
	moves = [x for x in moves if x != (p.ptype,p.x,p.y)]

	return moves


#BLACK PLAYER CONTAINS ONE PIECE (X)
#WHITE PLAYER CONTAINS TWO PIECE (Y)
#Generate total moves for player
def generateMoves(board, player):
	moves = []
	if player == "Y":
		moves.extend(genMovesKing(board.WK))
		if board.WR.capture == False:
			moves.extend(genMovesRook(board.WR))
	else:
		moves.extend(genMovesKing(board.BK))
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
				newBoard.BK.updatePos(child[1],child[2])
				val = search(newBoard,"Y", depth-1, False)	
			else:
				if child[0] == "WK":
					newBoard.WK.updatePos(child[1],child[2])
				else:
					newBoard.WR.updatePos(child[1],child[2])	
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
				newBoard.BK.updatePos(child[1],child[2])
				val = search(newBoard,"Y", depth-1, True)	
			else: 
				if child[0] == "WK":
					newBoard.WK.updatePos(child[1],child[2])
				else:
					newBoard.WR.updatePos(child[1],child[2])	
				val = search(newBoard,"X", depth-1, True)
			if val[1] < bestValue:
				bestValue = val[1]
				bestMove = child
		print (bestMove, bestValue)		
		return (bestMove, bestValue)			


temp = Board()
temp.BK.player = "X"
temp.BK.ptype = "BK"
temp.BK.x = 3
temp.BK.y = 3

temp.WR.player = "Y"
temp.WR.ptype = "WR"
temp.WR.x = 4
temp.WR.y = 6


temp.WK.player = "Y"
temp.WK.ptype = "WK"
temp.WK.x = 0
temp.WK.y = 0

print(search(temp, "Y",1,True))
print(search(temp, "X",2,True))
print(search(temp, "X",3,True))