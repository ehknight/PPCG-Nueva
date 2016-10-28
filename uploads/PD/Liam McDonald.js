main = function(currentRound,opHistory,myHistory){
  var cases = {wsw:0, wsl:0, wdw:0, wdl:0, lsw:0, lsl:0, ldw:0, ldl:0}
  var output = false;
  if(opHistory.length < 3){
    return false;
  }

  function win(i2){
    if(!opHistory[i] && myHistory[i] || opHistory[i] && opHistory[i]){
      return true;
    }else{
      return false;
  }

  for(i2 = 0; i+2 < opHistory; i++){
    if(win(i2)){
      if(opHistory[i+1] == opHistory[i]){
        if(win(i2+1)){
          if(opHistory[i+1] == opHistory[i+2]){
            cases.wsw++
          }else{
            cases.wsw--
          }
        }else{
          if(opHistory[i+1] == opHistory[i+2]){
            cases.wsl++
          }else{
            cases.wsl--
          }
        }
      }else{
        if(win(i2+1)){
          if(opHistory[i+1] == opHistory[i+2]){
            cases.wdw++
          }else{
            cases.wdw--
          }
        }else{
          if(opHistory[i+1] == opHistory[i+2]){
            cases.wdl++
          }else{
            cases.wdl--
          }
        }
      }

    }else{
      if(opHistory[i+1] == opHistory[i]){
        if(!opHistory[i+1] && myHistory[i+1] || opHistory[i+1] && opHistory[i+1]){
          if(opHistory[i+1] == opHistory[i+2]){
            cases.lsw++
          }else{
            cases.lsw--
          }
        }else{
          if(opHistory[i+1] == opHistory[i+2]){
            cases.lsl++
          }else{
            cases.lsl--
          }
        }
      }else{
        if(!opHistory[i+1] && myHistory[i+1] || opHistory[i+1] && opHistory[i+1]){
          if(opHistory[i+1] == opHistory[i+2]){
            cases.ldw++
          }else{
            cases.ldw--
          }
        }else{
          if(opHistory[i+1] == opHistory[i+2]){
            cases.ldl++
          }else{
            cases.ldl--
          }
        }
      }

    }
    i2 = opHistory.length - 2;
    if(win(i22)){
      if(opHistory[i+1] == opHistory[i]){
        if(win(i2+1)){
          if(cases.wsw > 1){
            output(1);
          }else if(cases.wsw < -1){
            output(2)
          }else{
            output(0)
          }
        }else{
          if(cases.wsl > 1){
            output(1);
          }else if(cases.wsl < -1){
            output(2)
          }else{
            output(0)
          }
        }
      }else{
        if(win(i2+1)){
          if(cases.wdw > 1){
            output(1);
          }else if(cases.wdw < -1){
            output(2)
          }else{
            output(0)
          }
        }else{
          if(cases.wdl > 1){
            output(1);
          }else if(cases.wdl < -1){
            output(2)
          }else{
            output(0)
          }
        }
      }
    }else{
      if(opHistory[i+1] == opHistory[i]){
        if(win(i2+1)){
          if(cases.lsw > 1){
            output(1);
          }else if(cases.lsw < -1){
            output(2)
          }else{
            output(0)
          }
          //lsw
        }else{
          if(cases.lsl > 1){
            output(1);
          }else if(cases.lsl < -1){
            output(2)
          }else{
            output(0)
          }
          //lsl
        }
      }else{
        if(win(i2+1)){
          if(cases.ldw > 1){
            output(1);
          }else if(cases.ldw < -1){
            output(2)
          }else{
            output(0)
          }
          //ldw
        }else{
          //ldl
          if(cases.ldl > 1){
            output(1);
          }else if(cases.ldl < -1){
            output(2)
          }else{
            output(0)
          }
          }
        }
      }

    }

    function output(defin){
      if(defin = 1){
        output = opHistory[opHistory.length-1];
      }else if(defin = 2){
        output = !opHistory[opHistory.length-1];
      }else{
        output = false;
      }
    }

    return output;


  } return false;

  }
