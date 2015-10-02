	
		
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




	



