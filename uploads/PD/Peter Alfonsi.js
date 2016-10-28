main = function(currentRound, opHistory, myHistory) {
  var ibetrayed = 0
  if (currentRound == 0) {
    return true
  }
  if (currentRound == 1) {
    return false
  }
  else if (Math.round(Math.random()*20) < currentRound && ibetrayed == 0) {
    return false
    ibetrayed == 1
  }
  return opHistory[opHistory.length - 1]
    
}
