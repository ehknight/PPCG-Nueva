main = function(currentRound, opHistory, myHistory){
    if(currentRound==0){
        return true
    }
    if(currentRound==1){
        return false
    }
    return opHistory[opHistory.length-1]
}
