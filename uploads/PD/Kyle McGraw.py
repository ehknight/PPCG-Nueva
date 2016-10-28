def main(rounds, opMoves, myMoves):
	tft = True
	for i in range(len(opMoves)-1):
		if (opMoves[i+1] != myMoves[i]):
			tft = False
	if tft and (len(opMoves)-1)>0:
		return True

	return False

# open Applications/*