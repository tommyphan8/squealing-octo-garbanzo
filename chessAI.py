
class Piece:
	def __int__(self, player, ptype, x, y):
		self.player = player
		self.ptype = ptype
		self.x = x
		self.y = y

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


def availableLocation(piece):
	available = []
	dangerZone = []
	if(piece.player == "x"):
		if(piece.ptype == "K"):
			available = piece.getSurrounding()

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

class Game:
	def __int__(self):
		self.WK = Piece()
		self.WR = Piece()
		self.BK = Piece()

	def addPiece(self,player,ptype,x,y):
		if(player == "x"):
			if(ptype == "K"):
				self.WK.setValue(player,ptype,x,y)
			else:
				self.WR.setValue(player,ptype,x,y)
		else:
			self.BK.setValue(player,ptype,x,y)

	def printState(self):
		printBoard(self.WK,self.WR, self.BK)

def main():
	test1 = Game()
	test1.addPiece("x","K",3,4)
	test1.addPiece("x","R",5,4)
	test1.addPiece("y","K",6,4)
	test1.printState()

	#WK = Piece()
	#WR = Piece()
	#BK = Piece()
	#WK.setValue("x","K",3,4)
	#WR.setValue("x","R",5,4)
	#BK.setValue("y","K",6,4)

	#k = rookway(WR)
	#print(k)
	#l = WK.getSurrounding()
	#print(l)
	#printBoard(WK,WR,BK)
	


main()


