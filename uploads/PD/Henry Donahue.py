def main(currentRound, opHistory, myHistory):
    if(currentRound==0):
        return False
    else:
        return opHistory[currentRound-1]
