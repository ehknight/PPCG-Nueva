main=function(currentRound, opHistory, myHistory){
    if(currentRound==0){
      return true
    }
    if(opHistory[opHistory.lenght-1]){
      return myHistory[myHistory.length-1]
    }
    if(myHistory[myHistory.length-1]==0){
      return true
    }
    if(myHistory[myHistory.length-1]==1){
    return false
    }
}
