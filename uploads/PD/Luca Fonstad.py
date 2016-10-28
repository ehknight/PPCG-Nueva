def main(round, opMoves, myMoves):
    if round==0:
        return False
    else:
        if opMoves[round-1]==0:
            return False
        else:
            return True
