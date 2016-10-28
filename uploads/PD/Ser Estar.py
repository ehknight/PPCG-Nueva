import random
def main(rounds, opMoves, myMoves):
    cache = [True,False,False,True]
    if rounds > len(cache) and opMoves[:len(cache)] == cache:
        if rounds > len(cache)+2 and 0 in opMoves[len(cache):]:
            return False
        return True
    return (random.random()<0.02)
# print main(8,[1,0,0,1,1,1,1],[1,1,1,1,1,1,1])
