var getExpectedValue, matrix, niceness, debug;

matrix = [[2, 5], [0, 1]];
debug = false;
niceness = 0;

getExpectedValue = function(opHistory) {
  var eP, eR, i, len, ps, rs;
  ps = ((function() {
    var j, len1, results;
    results = [];
    for (j = 0, len1 = opHistory.length; j < len1; j++) {
      i = opHistory[j];
      if (i === 1) {
        results.push(i);
      }
    }
    return results;
  })()).length;
  rs = ((function() {
    var j, len1, results;
    results = [];
    for (j = 0, len1 = opHistory.length; j < len1; j++) {
      i = opHistory[j];
      if (i === 0) {
        results.push(i);
      }
    }
    return results;
  })()).length;
  len = opHistory.length;
  eP = matrix[0][0] * (ps / len) + matrix[1][0] * (rs / len);
  eR = matrix[1][1] * (rs / len) + matrix[0][1] * (ps / len);
  return [eP, eR];
};

var arraysIdentical, fuzzyRecognize, recognizeTFT;

arraysIdentical = function(a, b) {
  var i;
  i = a.length;
  if (typeof(b)=='undefined') {
      return 0
  }
  if (i !== b.length) {
    return 0;
  }
  while (i--) {
    if (a[i] !== b[i]) {
      return 0;
    }
  }
  return 1;
};

fuzzyRecognize = function(mm, op) {
  var counter, index, j, ref;
  counter = 0;
  for (index = i = 0, ref = mm.length; 0 <= ref ? i <= ref : i >= ref; index = 0 <= ref ? ++i : --i) {
    if (mm[index] === op[index]) {
      counter += 1;
    }
  }
  return (counter-1)/(mm.length);
};

main = function(currentRound, opHistory, myHistory) {
  if (debug) {
    console.log('Moves so far for A: '+opHistory)
    console.log('Moves so far for B: '+myHistory)
  }
  var eP, eR, recents, recValue, rvalue, sliceValue, zeroArr, i, j;
  rvalue = 0
  if (currentRound === 1) {
    rvalue=1;
  } else {
    if (myHistory.slice(1)!=0) {
        recValue = fuzzyRecognize(myHistory.slice(0,-1),opHistory.slice(1))
        if (debug){
            console.log('Rec value is: '+recValue)
        }
    } else {
        recValue = 0
    }
    if (debug) {
        console.log('Slices compared are ['+(myHistory.slice(-4,-1))+'] | ['+(opHistory.slice(-3))+']')
        console.log('Fuzzy recognize is '+(fuzzyRecognize((myHistory.slice(-4,-1)),(opHistory.slice(-3)))))
    }
    zeroArr=new Array()
    sliceValue = 3
    for (i = j = 1, ref = sliceValue; 1 <= ref ? j <= ref : j >= ref; i = 1 <= ref ? ++j : --j) {
        zeroArr.push(0);
    }
    recents1 = myHistory.slice((-1*sliceValue-1),-1);
    recents2= opHistory.slice((-1*sliceValue));
    if ((recValue > 0.5) && (fuzzyRecognize(recents1,recents2)>.75) && !(arraysIdentical(opHistory.slice(-4),[0,0,0,0]))) {
        if (debug){
          console.log('+Found TFT!+');
        }
        rvalue=!(myHistory[myHistory.length-1])
    } else {
          eP = getExpectedValue(opHistory)[0];
          eR = getExpectedValue(opHistory)[1];
          if (eP + niceness > eR) {
            rvalue=1;
          } else {
            rvalue=0;
          }
    }
  }
  return rvalue
}
