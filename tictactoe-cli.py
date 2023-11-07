#    ____              _______       ______                          _____ __            ___
#   / __ \(_)  _____  / / ___/____  / __/ /__      ______ _________ / ___// /___  ______/ (_)___  _____
#  / /_/ / / |/_/ _ \/ /\__ \/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \\__ \/ __/ / / / __  / / __ \/ ___/
# / ____/ />  </  __/ /___/ / /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/__/ / /_/ /_/ / /_/ / / /_/ (__  )
#/_/   /_/_/|_|\___/_//____/\____/_/  \__/ |__/|__/\__,_/_/   \___/____/\__/\__,_/\__,_/_/\____/____/
#
# Started: 11/05/2023

# TODO:
#	Fix play again prompt to actually play again
#	Add curses to make graphical
#	
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
			for j, col in enumerate(row):
				piece = numToCharDict[col]
				if (i, j) in self.winningPlaces:  # Check if this position is part of the winning line
					drawnRow += f" {BOLD}{piece}{ENDC} │"
				else:
					drawnRow += f" {piece} │"

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
		for row_idx, row in enumerate(self.gameState):
			if -1 not in row:
				if len(set(row)) == 1:
					self.winningPlaces = [(row_idx, i) for i in range(boardSize)]
					return row[0]

		# Check vertically
		for col_idx in range(boardSize):
			col = [row[col_idx] for row in self.gameState]
			if -1 not in col:
				if len(set(col)) == 1:
					self.winningPlaces = [(i, col_idx) for i in range(boardSize)]
					return col[0]
		
		# Check left-right diagonal
		leftright = [self.gameState[i][i] for i in range(boardSize)]
		if -1 not in leftright:
			if len(set(leftright)) == 1:
				self.winningPlaces = [(i, i) for i in range(boardSize)]
				return leftright[0]

		# Check right-left diagonal
		rightleft = [self.gameState[i][boardSize - 1 - i] for i in range(boardSize)]
		if -1 not in rightleft:
			if len(set(rightleft)) == 1:
				self.winningPlaces = [(i, boardSize - 1 - i) for i in range(boardSize)]
				return rightleft[0]

		return -1
	
	def validateMove(self, move):
		if move.isdigit():
			move = int(move)
			if indexBasedMoves:
				if move < boardSize:
					return move
			elif move > 0 and move <= boardSize:
				return move
		
		return -1

	def makeMove(self, move):
		rowMove = -1
		colMove = -1

		#Sanitize and allow move to be collected in any format as long as it is row,col comma deliniated 
		if move:
			move = move.replace(" ", "")
			commaIdx = move.find(",")
			if commaIdx != -1 and commaIdx + 1 < len(move):
				rowMove = self.validateMove(move[commaIdx - 1])
				colMove = self.validateMove(move[commaIdx + 1])
		
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
					break

			else:
				print("Current Turn: " + self.currentTurn)
				move = input("\nYour Move: ")
				self.makeMove(move)
		
def main():
	# To make CLI text styling work on windows
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