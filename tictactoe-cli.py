#    ____              _______       ______                          _____ __            ___
#   / __ \(_)  _____  / / ___/____  / __/ /__      ______ _________ / ___// /___  ______/ (_)___  _____
#  / /_/ / / |/_/ _ \/ /\__ \/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \\__ \/ __/ / / / __  / / __ \/ ___/
# / ____/ />  </  __/ /___/ / /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/__/ / /_/ /_/ / /_/ / / /_/ (__  )
#/_/   /_/_/|_|\___/_//____/\____/_/  \__/ |__/|__/\__,_/_/   \___/____/\__/\__,_/\__,_/_/\____/____/
#
# Started: 11/05/2023

boardSize = 3

charToNumDict = {"O": 0, "X": 1}
numToCharDict = {-1: " ", 0: "O", 1: "X"}

currentGame = None

class TicTacToe:
	gameState = [[-1 for _ in range(boardSize)] for _ in range(boardSize)]
	currentTurn = "X"
	playerHasWon = False
	moveHistory = []

	# Initialize game state variables
	def newGame(self):
		self.gameState = [[-1 for _ in range(boardSize)] for _ in range(boardSize)]
		self.currentTurn = "X"
		self.playerHasWon = False
		self.moveHistory = []

	# Draw game board, allowing for any size board
	def drawGameState(self):
		fullDrawnState = "\n┌" + "───┬" * (boardSize - 1) + "───┐"
		for i, row in enumerate(self.gameState):
			drawnRow = "\n│"
			for col in row:
				drawnRow += f" {numToCharDict[col]} │"

			fullDrawnState += drawnRow
			if i < boardSize - 1:
				fullDrawnState += "\n├───" + "┼───" * (boardSize - 2) + "┼───┤" # Middle row markers
			else:
				fullDrawnState += "\n└" + "───┴" * (boardSize - 1) + "───┘" #End row marker

		print(fullDrawnState)

	def checkGameState(self):
		pass

	def makeMove(self, move):
		rowMove = -1
		colMove = -1

		#Sanitize and allow move to be collected in any format as long as it is row,col comma deliniated 
		if move:
			move = move.replace(" ", "")
			commaIdx = move.find(",")
			if commaIdx != -1 and commaIdx + 1 < len(move):
				potentialRowMove = move[commaIdx - 1]
				if potentialRowMove.isdigit():
					if int(potentialRowMove) < boardSize:
						rowMove = int(potentialRowMove)
				
				potentialColMove = move[commaIdx + 1]
				if potentialColMove.isdigit():
					if int(potentialColMove) < boardSize:
						colMove = int(potentialColMove)
		
		if rowMove != -1 and colMove != -1:
			#Execute move
			stateChange = charToNumDict[self.currentTurn]
			if self.gameState[rowMove][colMove] == -1 and stateChange:
				self.gameState[rowMove][colMove] = stateChange
				self.currentTurn = "X" if self.currentTurn == "O" else "O"
		else:
			print("Invalid move")

	def runGame(self):
		while not self.playerHasWon:
			self.drawGameState()
			print("Current Turn: " + self.currentTurn)
			move = input("\nYour Move: ")
			self.makeMove(move)
		


def main():
	print("TicTacToe CLI\n")
	print("Input your move in the format 'row, col', '0,0' being the top left corner")
	currentGame = TicTacToe()
	currentGame.runGame()
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nThanks for playing")