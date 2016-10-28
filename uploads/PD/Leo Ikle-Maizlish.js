main = function(currentRound, opHistory, myHistory){
    if(!currentRound||currentRound<14){
        if(opHistory[opHistory.length-1]){
            return true
        }
    }
    return false
}
