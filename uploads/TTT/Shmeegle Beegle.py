def main(team, board, currentBoard, metaBoard):
	return findMove(currentBoard[board[0]][board[1]])

def findMove(board, team):

	if board[1][1] == 0 or board[1][1] == 1:
		if board[2][2] == 0 or board[2][2] == 1:
			if board[2][1] == 0 or board[2][1] == 1:
				if board[2][0] == 0 or board[2][0] == 1:
					return [0, 1]
				return [2, 0]
			return [2,1]
		return [2, 2]
	return [1,1]

def pick(team, board, metaboard):
	return [1, 1]
