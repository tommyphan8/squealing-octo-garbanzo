import copy
import math
import sys
import random

king = 0
rook = 1
blank = (-1,-1)
black = 0
white = 1
debug = True
killed = 0
neg_infinity = -999999

class Piece:
	def __init__(self, color, ptype, x, y):
		self.color = color
		self.ptype = ptype
		self.x = x
		self.y = y

	def moveBlack(self, x, y, board_state):
		if self.color == black:
			if board_state.getSquare(x, y) != blank:
				board_state.take = True
				square = board_state.getSquare(x, y)
				killedPiece = board_state.getPiece(square[0], square[1])
				killedPiece.x = killed
				killedPiece.y = killed

			board_state.whoseTurn = white
		else:
			board_state.whoseTurn = black

		self.x = x
		self.y = y
	
	# return array of pairs
	def moveWhite(self, board_state):
		moves = []

		if self.ptype == rook:
			# advance right
			move_x = self.x + 1
			while move_x <= 8 and board_state.getSquare(move_x, self.y) == blank: 
				moves.append((move_x, self.y))
				move_x+=1

			# advance left
			move_x = self.x - 1
			while move_x > 0 and board_state.getSquare(move_x,self.y) == blank:
				moves.append((move_x, self.y))
				move_x-=1

			# advance up
			move_y = self.y + 1
			while move_y <= 8 and board_state.getSquare(self.x,move_y) == blank:
				moves.append((self.x, move_y))
				move_y+=1

			# advance down
			move_y = self.y - 1
			while move_y > 0 and board_state.getSquare(self.x,move_y) == blank:
				moves.append((self.x, move_y))
				move_y-=1

		elif self.ptype == king:
			invalid_positions = []

			if self.color == white:
				whiteRook = board_state.getPiece(white, rook)

				# Don't take out your own
				invalid_positions.append((whiteRook.x, whiteRook.y))

				opponent_king = board_state.getPiece(black, king)
			else:
				opponent_king = board_state.getPiece(white, king)
				whiteRook = board_state.getPiece(white, rook)
				move_x = whiteRook.x + 1
				while move_x <= 8 and (board_state.getSquare(move_x,whiteRook.y) == blank or board_state.getSquare(move_x,whiteRook.y) == (black, king)): 
					invalid_positions.append((move_x, whiteRook.y))
					move_x+=1

				move_x = whiteRook.x - 1
				while move_x > 0 and (board_state.getSquare(move_x,whiteRook.y) == blank or board_state.getSquare(move_x,whiteRook.y) == (black, king)):
					invalid_positions.append((move_x, whiteRook.y))
					move_x-=1

				move_y = whiteRook.y + 1
				while move_y <= 8 and (board_state.getSquare(whiteRook.x,move_y) == blank or board_state.getSquare(whiteRook.x,move_y) == (black, king)):
					invalid_positions.append((whiteRook.x, move_y))
					move_y+=1

				move_y = whiteRook.y - 1
				while move_y > 0 and (board_state.getSquare(whiteRook.x,move_y) == blank or board_state.getSquare(whiteRook.x,move_y) ==(black, king)):
					invalid_positions.append((whiteRook.x, move_y))
					move_y-=1
			
			invalid_positions.append((opponent_king.x+1, opponent_king.y+1))
			invalid_positions.append((opponent_king.x+1, opponent_king.y))
			invalid_positions.append((opponent_king.x+1, opponent_king.y-1))
			invalid_positions.append((opponent_king.x, opponent_king.y-1))
			invalid_positions.append((opponent_king.x-1, opponent_king.y-1))
			invalid_positions.append((opponent_king.x-1, opponent_king.y))
			invalid_positions.append((opponent_king.x-1, opponent_king.y+1))
			invalid_positions.append((opponent_king.x, opponent_king.y+1))

			if self.x+1 <= 8 and self.y+1 <= 8 and (self.x+1, self.y+1) not in invalid_positions:
				moves.append((self.x+1, self.y+1))
			if self.x+1 <= 8 and (self.x+1, self.y) not in invalid_positions:
				moves.append((self.x+1, self.y))
			if self.x+1 <= 8 and self.y-1 >= 1 and (self.x+1, self.y-1) not in invalid_positions:
				moves.append((self.x+1, self.y-1))
			if self.y-1 >= 1 and (self.x, self.y-1) not in invalid_positions:
				moves.append((self.x, self.y-1))
			if self.x-1 >= 1 and self.y-1 >= 1 and (self.x-1, self.y-1) not in invalid_positions:
				moves.append((self.x-1, self.y-1))
			if self.x-1 >= 1 and (self.x-1, self.y) not in invalid_positions:
				moves.append((self.x-1, self.y))
			if self.x-1 >= 1 and self.y+1 <= 8 and (self.x-1, self.y+1) not in invalid_positions:
				moves.append((self.x-1, self.y+1))
			if self.y+1 <= 8 and (self.x, self.y+1) not in invalid_positions:
				moves.append((self.x, self.y+1))
		return moves

	def surroundingSquares(self):
		return [(self.x+1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1), (self.x, self.y+1), (self.x, self.y-1), (self.x+1, self.y), (self.x-1, self.y)]

class Board:
	def __init__(self):
		self.blackPieces = []
		self.whitePieces = []
		self.whoseTurn = black
		self.take = False

	def print(self):
		for y in range(8, 0, -1):
			print(str(y) + ' |', end="")
			for x in range(1, 9):
				if self.getSquare(x,y) == blank:
					print('__|', end="")
				elif self.getSquare(x,y) == (black, king):
					print('BK|', end="")
				elif self.getSquare(x,y) == (white, king):
					print('WK|', end="")
				elif self.getSquare(x,y) == (white, rook):
					print('WR|', end="")
			print()
		print('   1  2  3  4  5  6  7  8\n')

	def randomheuristicY(self):
		return random.randrange(0, 101)

	def randomheuristicX(self):
		return random.randrange(0, 101)

	def heuristicY(self):
		heuristic = 0
		center = [(4,4),(4,5),(5,4),(5,5)]
		blackKing = self.getPiece(black, king)
		whiteKing = self.getPiece(white, king)
		whiteRook = self.getPiece(white, rook)
		#if black king is adjacent to the rook:
			#if rook is not adjacent to white king:
				#black king eats rook
		#elif white king far from white rook:
		if debug:
			print("moveWhite: BK:", (blackKing.x, blackKing.y), " WK:", (whiteKing.x, whiteKing.y), " WR:", (whiteRook.x, whiteRook.y), "= " , end='')
		if self.isCheckmate():
			heuristic = 100
		else:
				#moveBlack black king closer to rook:
		#elif white king closer to the white rook
			#if black king can moveBlack to center:
				#moveBlack close to center
			if (blackKing.x,blackKing.y) in center:
				heuristic +=8
				#elif rook  or white king blocking the path to center:
			#moveBlack the black king to the direction farther to the edge
			elif (blackKing.x,blackKing.y) in whiteRook.surroundingSquares() and whiteRook.surroundingSquares() in whiteKing.surroundingSquares():
				heuristic +=8	
			else:
			# else:
				# moveBlack white king closer to black king
				heuristic += (8 - math.sqrt((whiteKing.x - blackKing.x)**2 + (whiteKing.y - blackKing.y)**2))
			if debug:
				print(heuristic)	
			return heuristic

	def heuristicX(self):
		blackKing = self.getPiece(black, king)
		whiteKing = self.getPiece(white, king)
		whiteRook = self.getPiece(white, rook)
		if debug:
			print("moveWhite: BK:", (blackKing.x, blackKing.y), " WK:", (whiteKing.x, whiteKing.y), " WR:", (whiteRook.x, whiteRook.y), "= " , end='')
		heuristic = 0
		# Goal State found
		if self.isCheckmate():
			print("checkmate")
			heuristic = 1000
		# Evaluating Search Space
		else:
		# elif (blackKing.x, blackKing.y) in [(1,1),(1,8),(8,1),(8,8)]:
			#heuristic+=8
			# Sweet spots are marked by X
			#
			# 8 |__|__|__|__|__|__|__|__|
			# 7 |__|__|X_|__|__|X_|__|__|
			# 6 |__|X_|__|__|__|__|X_|__|
			# 5 |__|__|__|__|__|__|__|__|
			# 4 |__|__|__|__|__|__|__|__|
			# 3 |__|X_|__|__|__|__|X_|__|
			# 2 |__|__|X |__|__|X_|__|__|
			# 1 |__|__|__|__|__|__|__|__|
			#    1  2  3  4  5  6  7  8
			sweetSpots = [(3,2),(2,3),(2,6),(3,7),(6,2),(7,3),(6,7),(7,6)]
			# States where the black king in a corner:
			### START BOTTOM LEFT ###
						# elif white king adjacent to sweet spot close to black king corner:
			#elif (whiteKing.x, whiteKing.y) in [(1,3),(1,4),(2,4),(3,4),(3,3),(4,3),(4,2),(4,1),(3,1)] and (blackKing.x, blackKing.y) == (1,1):
				# moveBlack white king to sweet spot
				#if (whiteKing.x, whiteKing.y) in sweetSpots:
			# if white king in sweet spot close to black king corner:
			if (blackKing.x, blackKing.y) in [(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)] and (whiteKing.x, whiteKing.y) in [(2,3),(3,2)]:
				#print("bottom left corner")
				heuristic = 800
				# if white rook in (same x-axis or same y-axis) as white king:
				if whiteRook.x != whiteKing.x and whiteRook.y != whiteKing.y:
					heuristic+=8
					# moveBlack white king to other sweet spot
					if (whiteKing.x, whiteKing.y) in sweetSpots:
						heuristic+=8
				# elif white king is in closer horizontal sweet spot:		
				elif (whiteKing.x, whiteKing.y) == (2,3):
					heuristic+=8
					# moveBlack white rook to same y-axis as black king and not adjacent to black king
					if whiteRook.y == blackKing.y:
						heuristic+=8
			## END BOTTOM LEFT ##
			## START TOP RIGHT ##
			elif (blackKing.x, blackKing.y) in [(6,8),(7,8),(7,7),(8,8),(8,7),(8,6)] and (whiteKing.x, whiteKing.y) in [(6,7),(7,6)]:
				#print("top right corner")
				heuristic = 800
				# if white rook in (same x-axis or same y-axis) as white king:
				if whiteRook.x != whiteKing.x and whiteRook.y != whiteKing.y:
					heuristic+=8
					# moveBlack white king to other sweet spot
					if (whiteKing.x, whiteKing.y) in sweetSpots:
						heuristic+=8
				# elif white king is in closer horizontal sweet spot:		
				elif (whiteKing.x, whiteKing.y) == (7,6):
					heuristic+=8
					# moveBlack white rook to same y-axis as black king and not adjacent to black king
					if whiteRook.y == blackKing.y:
						heuristic+=8
			## END TOP RIGHT ##
			### START BOTTOM RIGHT  ###
			# if black king in corner:
			# if white king in sweet spot close to black king corner:
			elif (blackKing.x, blackKing.y) in [(8,1),(7,1),(6,1),(8,2),(8,3),(7,2)] and (whiteKing.x, whiteKing.y) in [(7,3),(6,2)]:
				#print("bottom right corner")
				heuristic = 800
				# if white rook in (same x-axis or same y-axis) as white king:
				if whiteRook.x != whiteKing.x and whiteRook.y != whiteKing.y:
					heuristic+=8
					# moveBlack white king to other sweet spot
					if (whiteKing.x, whiteKing.y) in sweetSpots:
						heuristic+=8
				# elif white king is in closer horizontal sweet spot:		
				elif (whiteKing.x, whiteKing.y) == (7,3):
					heuristic+=8
					# moveBlack white rook to same y-axis as black king and not adjacent to black king
					if whiteRook.y == blackKing.y:
						heuristic+=8
			### END BOTTOM RIGHT ###
			### START TOP LEFT ###
			# if white king in sweet spot close to black king corner:
			elif (blackKing.x, blackKing.y) in [(1,8),(1,7),(1,6),(2,8),(3,8),(2,7)] and (whiteKing.x, whiteKing.y) in [(2,6),(3,7)]:
				#print("bottom left corner")
				heuristic = 800
				# if white rook in (same x-axis or same y-axis) as white king:
				if whiteRook.x != whiteKing.x and whiteRook.y != whiteKing.y:
					heuristic+=8
					# moveBlack white king to other sweet spot
					if (whiteKing.x, whiteKing.y) in sweetSpots:
						heuristic+=8
				# elif white king is in closer horizontal sweet spot:		
				elif (whiteKing.x, whiteKing.y) == (2,6):
					heuristic+=8
					# moveBlack white rook to same y-axis as black king and not adjacent to black king
					if whiteRook.y == blackKing.y:
						heuristic+=8
			### END BOTTOM LEFT ###
			# else:
			# State where white rook is adjacent to black king and white king is not within adjacent cells:
			elif (whiteRook.x, whiteRook.y) in blackKing.moveWhite(self) and (whiteRook.x, whiteRook.y) not in whiteKing.surroundingSquares():
				heuristic = -200
			else:
			#elif not (whiteRook.x, whiteRook.y) in blackKing.moveWhite(self):
				#don't put rook in danger position
				if whiteRook.moveWhite(self) not in blackKing.surroundingSquares():
					#print("don't put rook in danger position")
					heuristic = 600
					if blackKing.x < whiteRook.x and blackKing.y < whiteRook.y:
						heuristic -= (whiteRook.x - 1) * (whiteRook.y - 1) - 10
					elif blackKing.x < whiteRook.x and blackKing.y > whiteRook.y:
						heuristic -= (whiteRook.x - 1) * (8 - whiteRook.y) - 10
					elif blackKing.x > whiteRook.x and blackKing.y < whiteRook.y:
						heuristic -= (8 - whiteRook.x) * (whiteRook.y - 1) - 10
					elif blackKing.x > whiteRook.x and blackKing.y > whiteRook.y:
						heuristic -= (8 - whiteRook.x) * (8 - whiteRook.y) - 10
					heuristic += (8 - math.sqrt((whiteKing.x - blackKing.x)**2 + (whiteKing.y - blackKing.y)**2))
		if debug:
			print(heuristic)
		return heuristic

	def addPiece(self, color, piece, x, y):
		new_piece = Piece(color, piece, x, y)
		if color == black:
			blackPieces.append(new_piece)
		else: 
			whitePieces.append(new_piece)

	def getPiece(self, color, piece):
		if color == white:
			if self.whitePieces[0].ptype == piece:
				return self.whitePieces[0]
			else:
				return self.whitePieces[1]
		else:
			return self.blackPieces[0]

	def getSquare(self, x, y):
		for piece in self.whitePieces + self.blackPieces:
			if (piece.x, piece.y) == (x, y):
				return (piece.color, piece.ptype)
		return blank

	def isCheck(self):
		# White's turn
		# Because black only has a king, it can not put white in check.
		if self.whoseTurn == white:
			return False
		# Black's turn
		else:
			# White lost its rook so white can no longer check.
			if len(self.whitePieces) == 1:
				return False
			# Is the black king checked by the white rook?
			whiteRook = self.getPiece(white, rook)
			blackKing = self.getPiece(black, king)
			# White Rook in the same row or column as Black King
			if whiteRook.x != blackKing.x and whiteRook.y != blackKing.y:
				return False
			# Is white king blocking white rook from checking
			whiteKing = self.getPiece(white, king)
			if whiteRook.x == blackKing.x and whiteRook.x == whiteKing.x and ((whiteKing.y < whiteRook.y and whiteKing.y > blackKing.y) or (whiteKing.y < whiteRook.y and whiteKing.y > blackKing.y)):
				return False
			if whiteRook.y == blackKing.y and whiteRook.y == whiteKing.y and ((whiteKing.x < whiteRook.x and whiteKing.x > blackKing.x) or (whiteKing.x < whiteRook.x and whiteKing.x > blackKing.x)):
				return False
		return True

	def isCheckmate(self):
		if self.whoseTurn == black:
			OpponentsKing = self.getPiece(black, king)
		else:
			OpponentsKing = self.getPiece(white, king)
		if len(OpponentsKing.moveWhite(self)) == 0 and self.isCheck():
			return True
		return False
class Chess:
	def __init__(self):
		self.current_state = Board()

	def addPiece(self, color, piece, x, y):
		if color == black:
			new_piece = Piece(color, piece, x, y)
			self.current_state.blackPieces.append(new_piece)
		else:
			new_piece = Piece(color, piece, x, y)
			self.current_state.whitePieces.append(new_piece)

	def play(self, moves, randomBlack=False):
		print("Initial Board")
		self.current_state.print()
		for i in range(moves):
			# White Moves
			best_state_value = neg_infinity
			search_state = copy.deepcopy(self.current_state)
			moved = False
			for whitePiece in search_state.whitePieces:
				if debug:
					print("Piece at", (whitePiece.x, whitePiece.y), end='')
				OriginalPosition = (whitePiece.x, whitePiece.y)
				if debug:
					print(" should have", len(whitePiece.moveWhite(search_state)), "possible moves.")
				for whiteMove in whitePiece.moveWhite(search_state):
					whitePiece.moveBlack(whiteMove[0], whiteMove[1], search_state)
					moved = True
					heuristic=search_state.heuristicX()
					if heuristic > best_state_value:
						best_state_value = heuristic
						PreviousPosition = copy.deepcopy(OriginalPosition)
						NewPosition = (whiteMove[0], whiteMove[1])
						MovedPiece = whitePiece.ptype
						BestState = copy.deepcopy(search_state)
				# moveBlack previous piece back to its original spot before testing the next piece
				whitePiece.moveBlack(OriginalPosition[0], OriginalPosition[1], search_state)
			self.current_state = copy.deepcopy(BestState)
			if not moved:
				print("Number of moves made: "+ str(i+1))
				print("Game result: Checkmate! White Wins")
				return
			if MovedPiece == rook:
				print("White's Turn " + str(i+1) + " of " + str(moves) + " - White rook moves from ", end="")
			else:
				print("White's Turn " + str(i+1) + " of " + str(moves) + " - White king moves from ", end="")
			print(str(PreviousPosition) + " to " + str(NewPosition), end="")
			if self.current_state.isCheck():
				print(" - Check!")
			else:
				print()
			self.current_state.print()
			# Black Moves			
			best_state_value = neg_infinity
			search_state = copy.deepcopy(self.current_state)
			moved = False

			for blackPiece in search_state.blackPieces:
				# original = copy.deepcopy(blackPiece)
				position = (blackPiece.x, blackPiece.y)
				for blackMove in blackPiece.moveWhite(search_state):
					blackPiece.moveBlack(blackMove[0], blackMove[1], search_state)
					moved = True
					if randomBlack:
						heuristic = search_state.randomheuristicY();
					else:
						heuristic = search_state.heuristicY();

					if heuristic > best_state_value or search_state.take:
						best_state_value = heuristic
						PreviousPosition = copy.deepcopy(position)
						NewPosition = (blackMove[0], blackMove[1])
						self.current_state = copy.deepcopy(search_state)
						if search_state.take:
							break
					# blackPiece = copy.deepcopy(original)
			# Game Ends: There is no possible moves
			if not moved:
				if self.current_state.isCheck():
					print("Number of moves made: "+ str(i+1))
					print("Game result: Checkmate! White Wins")
				else:
					print("Number of moves made: "+ str(i+1))
					print("Game result: Stalemate")
				return
			print("Black's Turn " + str(i+1) + " of " + str(moves) + " - Black king moves from " + str(PreviousPosition) + " to " + str(NewPosition))
			self.current_state.print()

			if self.current_state.take == True:
				print("Number of moves made: "+ str(i+1))
				print("Game result: Stalemate")
				return
		print("Number of moves made: "+ str(i+1))		
		print("Game result: Draw. No moves left.")

def main():
	fd = open('output.txt','w') # open the result file in write mode
	old_stdout = sys.stdout   # store the default system handler to be able to restore it
	sys.stdout = fd # Now your file is used by print as destination 
	#print("------ GAME 1 ------")
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 1 : w(5,6), r(8,5), b(6,8)")
	print("Heuristic function used: heuristicX")	
	print("-------------------------------------------")
	game1 = Chess()
	game1.addPiece(white, king, 5, 6)
	game1.addPiece(white, rook, 8, 5)
	game1.addPiece(black, king, 6, 8)
	game1.play(35,True)

	#print("------ GAME 2 ------")
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 2 : w(6.5), r(5,6), b(4,7)")
	print("Heuristic function used: heuristicX")
	print("-------------------------------------------")
	game2 = Chess()
	game2.addPiece(white, king, 6, 5)
	game2.addPiece(white, rook, 5, 6)
	game2.addPiece(black, king, 4, 7)
	game2.play(35,True)

	#print("------ GAME 3 ------")
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 3 : w(7,6), r(8,5), b(7,8)")
	print("Heuristic function used: heuristicX")
	print("-------------------------------------------")
	game3 = Chess()
	game3.addPiece(white, king, 7, 6)
	game3.addPiece(white, rook, 8, 5)
	game3.addPiece(black, king, 7, 8)
	game3.play(35,True)

	game4 = Chess()
	#print("-------Game 4 --------")	
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 4 : w(5,6), r(8,5), b(6,8)")
	print("Heuristic function used: heuristicX and heuristicY")
	print("-------------------------------------------")
	game4.addPiece(white, king, 5, 6)
	game4.addPiece(white, rook, 8, 5)
	game4.addPiece(black, king, 6, 8)
	game4.play(35,False)

	#print("------ GAME 5 ------")
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 5 : w(6.5), r(5,6), b(4,7)")
	print("Heuristic function used: heuristicX and heuristicY")
	print("-------------------------------------------")
	game5 = Chess()
	game5.addPiece(white, king, 6, 5)
	game5.addPiece(white, rook, 5, 6)
	game5.addPiece(black, king, 4, 7)
	game5.play(35,False)

		#print("------ GAME 6 ------")
	print("-------------------------------------------")
	print("Game started...")
	print("Testcase 6 : w(7,6), r(8,5), b(7,8)")
	print("Heuristic function used: heuristicX and heuristicY")
	print("-------------------------------------------")
	game6 = Chess()
	game6.addPiece(white, king, 7, 6)
	game6.addPiece(white, rook, 8, 5)
	game6.addPiece(black, king, 7, 8)
	game6.play(35,False)

	sys.stdout=old_stdout # here we restore the default behavior
	fd.close()

if __name__ == '__main__':
	main()
