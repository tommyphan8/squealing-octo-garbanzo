import math
import sys

#const values for king and rook
KING = 0
ROOK = 1
#const values for player X and Y
X = 0
Y = 1


class Piece:
	def __init__(self, player, ptype, x, y):
		self.player = player
		self.ptype = ptype
		self.x = x
		self.y = y

        #return locations around this piece
	def getSurrounding(self):
		return [(self.x+1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1), (self.x, self.y+1), (self.x, self.y-1), (self.x+1, self.y), (self.x-1, self.y)]

        #return locations cover by a rook
	def rookway(self):
		locations = []
		for i in range(0,8):
			locations.append((i, self.y))
			locations.append((self.x, i))
		return locations

                        

class Board:
        def __init__(self):
                self.playerX = []
                self.playerY = []
                XK

        # add piece for each player
        def addPiece(self, player, ptype, x, y): 
                temp = Piece(player, ptype, x, y)
                if player == X:
                        playerX.append(temp)
                else:
                        playerY.append(temp)

        def getPiece(self, player, ptype):
                if player == X:
                        if self.playerX[0].ptype == K:
                                return self.playerX[0]
                        else:
                                return self.playerX[1]
                else:
                        return self.playerY[0]




class Game:
        def __int__(self):
                self.board = Board()

        def addPiece(self, player, ptype, x, y):
                if player == X:
                        self.board.playerX.addPiece(X, ptype, x, y)
                else
                        self.board.playerY.addPiece(Y, ptype, x, y)

        def availLocations(self, player, ptype):
                available =[]
                dangerZone = []
                if(player == X):
                        if(ptype == K):
                                available = self.board.playerX[0].getSurrounding()
                        else:
                                available = self.board.playerX[1].rookway()
                        return available - self.board.playerY[0].getSurrounding()
                else:
                        available = self.board.playerY[0].getSurrounding()
                        return available - self.board.playerX[0].getSurrounding() - self.board.playerX[1].rookway()



        
    
