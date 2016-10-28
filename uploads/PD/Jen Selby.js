main = function(currentRound, opHistory, myHistory){
    if (   opHistory.length >= 2
        && opHistory[opHistory.length - 1] == 0
        && opHistory[opHistory.length - 2] == 0) {
         return false;
    }
 
    return true;
}
