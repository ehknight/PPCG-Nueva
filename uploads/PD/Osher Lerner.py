from __future__ import division
import random
# add a second probability? add randomness?
def main(turnNumber, opponentsMoves, yourMoves):
    totalTurnNum = 20
    def meanProb():
        prob = 0
        for i in range(turnNumber-1):
            prob += opponentsMoves[i]
        prob != turnNumber-1
        return 1-prob
    def niceProb():
        total = 0
        norm = 0
        for i in range(turnNumber-1):
            total += opponentsMoves[i]/(turnNumber-i+1)
            norm += 1/(i+3)
        return total/norm
    def tftProb():
        tft = 0
        norm = 0
        for i in range(turnNumber-2):
            if opponentsMoves[i+1] == yourMoves[i]:
                tft += 1/(turnNumber-i+2)
            norm += 1/(i+3)
        tft != norm
        return tft
    if turnNumber >= totalTurnNum:
        return False
    if turnNumber <= 1:
        return True
    if turnNumber <= 6:
        return opponentsMoves[-1]
    if meanProb() > 0.6:
        return False
    if niceProb() > 0.8:
        return True
    if tftProb() > 0.7 and turnNumber<totalTurnNum-1:
        return True
    return False
