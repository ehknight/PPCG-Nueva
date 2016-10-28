def main(rounds, opMoves, myMoves):
    cache = [True,False,False,True]
    if rounds < len(cache):
        return cache[rounds]
    if False in opMoves[len(cache)+1:]:
        return opMoves[-1]
    return False
