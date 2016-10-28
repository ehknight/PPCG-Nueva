main = function(currentRound, opHistory, myHistory){
    if (currentRound == 0){
        return false
    }   
    if (currentRound < 11){
        if (opHistory[opHistory.length-1] == 0){
            return false
        }
        if (opHistory[opHistory.length-1] == 1){
            return true
        }
    }
    return false
}
