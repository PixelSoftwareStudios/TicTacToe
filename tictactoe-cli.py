#    ____              _______       ______                          _____ __            ___
#   / __ \(_)  _____  / / ___/____  / __/ /__      ______ _________ / ___// /___  ______/ (_)___  _____
#  / /_/ / / |/_/ _ \/ /\__ \/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \\__ \/ __/ / / / __  / / __ \/ ___/
# / ____/ />  </  __/ /___/ / /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/__/ / /_/ /_/ / /_/ / / /_/ (__  )
#/_/   /_/_/|_|\___/_//____/\____/_/  \__/ |__/|__/\__,_/_/   \___/____/\__/\__,_/\__,_/_/\____/____/
#
# Started: 11/05/2023

import os

# Settings
boardSize = 3
indexBasedMoves = False

charToNumDict = {"O": 0, "X": 1}
numToCharDict = {-1: " ", 0: "O", 1: "X"}

emptyGameState = [[-1 for _ in range(boardSize)] for _ in range(boardSize)]

#style
ENDC = '\033[0m'
BOLD = '\033[1m'

class TicTacToe:
	gameState = [x[:] for x in emptyGameState]
	currentTurn = "X"
	playerHasWon = False
	winner = None
	winningPlaces = []
	moveHistory = []

	# Initialize game state variables
	def newGame(self):
		self.gameState = [x[:] for x in emptyGameState]
		self.currentTurn = "X"
		self.playerHasWon = False
		self.winner = None
		self.winningPlaces = []
		self.moveHistory = []

	# Draw game board, allowing for any size board
	def drawGameState(self):
		fullDrawnState = "\n┌" + "───┬" * (boardSize - 1) + "───┐"
		for i, row in enumerate(self.gameState):
			drawnRow = "\n│"
			for col in row:
				piece = numToCharDict[col]
				if self.winner == piece:
					drawnRow += f" {BOLD}{numToCharDict[col]}{ENDC} │"
				else:
					drawnRow += f" {numToCharDict[col]} │"

			fullDrawnState += drawnRow
			if i < boardSize - 1:
				fullDrawnState += "\n├───" + "┼───" * (boardSize - 2) + "┼───┤" # Middle row markers
			else:
				fullDrawnState += "\n└" + "───┴" * (boardSize - 1) + "───┘" #End row marker

		print(fullDrawnState)

	def checkWinner(self):
		# Return early if board empty
		if self.gameState == emptyGameState:
			return -1

		# Check whole board for draw
		if all(-1 not in row for row in self.gameState):
			return "draw"

		# Check horizontally
		for row in self.gameState:
			row = set(row)
			if -1 not in row:
				if len(set(row)) == 1:
					return row.pop()

		# Check vertically
		for i in range(boardSize):
			col = set([row[i] for row in self.gameState])
			if -1 not in col:
				if len(col) == 1:
					return col.pop()
		
		# Check left-right diagonal
		leftright = set([self.gameState[i][i] for i in range(boardSize)])
		if -1 not in leftright:
			if len(leftright) == 1:
				return self.gameState[0][0]

		# Check right-left diagonal
		rightleft = set([self.gameState[i][boardSize - 1 - i] for i in range(boardSize)])
		if -1 not in rightleft:
			if len(rightleft) == 1:
				return self.gameState[0][boardSize - 1]

		return -1

	def makeMove(self, move):
		rowMove = -1
		colMove = -1

		#Sanitize and allow move to be collected in any format as long as it is row,col comma deliniated 
		if move:
			move = move.replace(" ", "")
			commaIdx = move.find(",")
			if commaIdx != -1 and commaIdx + 1 < len(move):
				# p means potential, this is so I only need to print invalid move once
				pRowMove = move[commaIdx - 1]
				if pRowMove.isdigit():
					pRowMove = int(pRowMove)
					if indexBasedMoves:
						if pRowMove < boardSize:
							rowMove = pRowMove
					elif pRowMove > 0 and pRowMove <= boardSize:
						rowMove = pRowMove
				
				pColMove = move[commaIdx + 1]
				if pColMove.isdigit():
					pColMove = int(pColMove)
					if indexBasedMoves:
						if pColMove < boardSize:
							colMove = pColMove
					elif pColMove > 0 and pColMove <= boardSize:
						colMove = pColMove
		
		#Validate and execute move
		if rowMove != -1 and colMove != -1:
			stateChange = charToNumDict[self.currentTurn]

			if not indexBasedMoves:
				rowMove -= 1 # Reduce by one for list indexing
				colMove -= 1

			if self.gameState[rowMove][colMove] == -1 and stateChange != None:
				self.gameState[rowMove][colMove] = stateChange

				self.moveHistory.append([self.currentTurn, (rowMove, colMove)])
				self.currentTurn = "X" if self.currentTurn == "O" else "O"
			else:
				print("Invalid move: space occupied")
		else:
			print("Invalid move")

	def runGame(self):
		while not self.playerHasWon:
			check = self.checkWinner()
			if check != -1:
				# feel like I could do this part better
				if check != "draw":
					self.winner = numToCharDict[check]
				else:
					self.winner = "draw"

				self.playerHasWon = True

			self.drawGameState()

			if self.playerHasWon:
				if self.winner == "draw":
					print("You went to a draw, what a surprise")
				else:
					print(self.winner + " wins!")
				
				again = input("\nWould you like to play again (y/n): ")
				again = again.lower()
				if again == "y" or again == "yes":
					self.newGame()

			else:
				print("Current Turn: " + self.currentTurn)
				move = input("\nYour Move: ")
				self.makeMove(move)
		
def main():
	# To make cmd formatting work on windows
	if os.name == 'nt':
		os.system("color")

	print("TicTacToe CLI\n")
	print(f"Input your move in the format 'row, col', '{'0,0' if indexBasedMoves else '1,1'}' being the top left corner")
	
	game = TicTacToe()
	game.runGame()
	
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nThanks for playing")