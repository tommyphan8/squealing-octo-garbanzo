import math	
		
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
		self.player = ""
		self.ptype = ""
		self.x = -1
		self.y = -1

	def setValue(self,player,ptype,x,y):
		self.player = player
		self.ptype = ptype
		self.x = x
		self.y = y

	def updateLocation(self,x,y):
		self.x = x
		self.y = y

	def printPiece(self):
		print(self.player,self.ptype,"(",self.x,",",self.y,")")

	def getSurrounding(self):
		return [(self.x+1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1), (self.x, self.y+1), (self.x, self.y-1), (self.x+1, self.y), (self.x-1, self.y)]

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

	def availableLocation(self,piece):
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
					return FALSE
				else: 
					return TRUE
			else:
				if((self.WK.x, self.WK.y) in dangerZone):
					return FALSE
				else:
					return TRUE
		





def printBoard(xK,xR,yK):
    print("+----+----+----+----+----+----+----+----+")
    for i in range(1,9):
        for j in range(1,9):
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

#Player x is white 
#Player y is black
def heustric(white, black):
	blackScore = 0
	whiteScore = 0

	for i in black:
		if i.ptype == "KING":
			blackScore += King
			blackScore += pieceSquareTableKing[i.y][i.x]
		else:
			blackScore += Rook
			blackScore += pieceSquareTableRook[i.y][i.x]

	for  j in white:
		if j.ptype == "KING":	
			whiteScore += King
			whiteScore += pieceSquareTableKing[abs((j.y)-7)][j.x]
			#whiteScore += pieceSquareTableKing[abs(i.y-7)][i.x]
		else:
			whiteScore += Rook
			whiteScore += pieceSquareTableRook[abs(j.y-7)][j.x]

	return blackScore -	whiteScore


                        
#Generate possible moves for input:piece
def genMovesKing(p, moves):
	moves.extend((("KING",p.x-1, p.y), ("KING",p.x+1,p.y), ("KING",p.x,p.y+1), ("KING",p.x-1,p.y+1), ("KING",p.x+1, p.y+1), ("KING",p.x, p.y-1), ("KING",p.x+1, p.y-1), ("KING",p.x-1, p.y-1)))
	
	#filter out pieces that are out the boundary
	moves = [x for x in moves if x[1] >= 0 and x[1] <= 7 ]
	moves = [x for x in moves if x[2] >= 0 and x[2] <= 7]
			
	#return moves

#Generate possible moves for input:piece
def genMovesRook(p, moves):
	#moves = []
	for i in range(0,8):
		moves.append(("ROOK",p.x,i))

	for i in range(0,8):
		moves.append(("ROOK",i,p.y))

	moves = [x for x in moves if x != ("ROOK",p.x,p.y)]

	#return moves

#Generate total moves for player
def generateMoves(board, player):
	moves = []
	if player == "X":
		for x in board.playerX:
			if x.ptype == "ROOK":
				genMovesRook(x,moves)
			elif x.ptype == "KING":
				genMovesKing(x,moves)

	else:
		for x in board.playerY:
			if x.ptype == "ROOK":
				genMovesRook(x,moves)
			elif x.pype == "KING":
				genMovesKing(x,moves)
	return moves


def search(Piece, game, depth, maxPlayer):
	if depth == 0: 
		return heustric(node)
	if maxPlayer == TRUE:
		bestValue = -math.inf
		for child in getMoveKing(node):
			val = search(child, depth -1, FALSE)
			if val > bestValue:
				bestValue = val
	else:
		bestValue = math.inf
		for child in getMoveKing(node):
			val = minimax(child, depth -1, TRUE)
			if val < bestValue:
				return bestValue





temp = Board()
temp.addPiece("X","ROOK",4,3)
temp.addPiece("X","KING",4,2)
temp.addPiece("Y","KING",7,5)
temp.printState()
print(temp.availableLocation(temp.WK))
