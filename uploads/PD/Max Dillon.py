def main(rounds, opMoves, myMoves):
    cache = [True,False,False,True]
    if rounds > len(cache) and opMoves[:len(cache)] == cache:
        return True
    return False
