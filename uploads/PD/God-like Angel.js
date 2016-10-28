main=function(currentRound, myHistory, opHistory){
if(currentRound == 0){
    return true;
}
if(opHistory[opHistory.length-1] == false){
    return false;
}
if(opHistory[opHistory.length-2] == false){
    return false;
}
return true;
};