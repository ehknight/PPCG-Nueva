exports.method = function(currentRound, opHistory, myHistory){
    if opHistory[opHistory.length-1] == 0 and opHistory[opHistory.length-2] == 0:
        return false
    return true
}