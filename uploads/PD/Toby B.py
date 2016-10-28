from random import randint

def main(currentRound, myHistory, opHistory):
    totalTrue = 0
    totalFalse = 0
    for i in range(0, currentRound):
        if opHistory[i]:
            totalTrue ++ 1
        else:
            totalFalse ++ 1
    if currentRound != 0:
        percentTrue = round ((totalTrue/currentRound) * 100)
        percentFalse = round ((totalFalse/currentRound) * 100)
    else:
        return False
    if percentTrue < percentFalse:
        return True
    else:
        return False
