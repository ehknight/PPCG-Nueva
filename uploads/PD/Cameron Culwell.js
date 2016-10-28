main = function(currentRound, opHistory, myHistory){
    if (currentRound == 0){
        return true
    }
    if (currentRound == 2){
        var random = Math.random()
        if (random < .33){
            return true
        }
        if (random > .33){
            return false
      }
    }
    if (currentRound == 5){
        return opHistory[3]
    }
    if (currentRound == 9){
      var toSelectRandomFrom = new Array(1,3,5,7)
      var randomIndex = Math.round(Math.random() * toSelectRandomFrom.length) - 1
      return opHistory[toSelectRandomFrom[randomIndex]]
      if (!currentRound % 2){
        toSelectRandomFrom.append(currentRound)
      }
    }
}
