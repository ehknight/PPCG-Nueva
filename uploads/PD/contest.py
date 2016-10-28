import os, sys
import js2py
import types
import signal
from random import randrange

class SeemsToWork(Exception):
    pass

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

debug = False

def copy_func(f, name=None):
    #https://stackoverflow.com/questions/6527633/how-can-i-make-a-deepcopy-of-a-function-in-python
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
        f.func_defaults, f.func_closure)


def Comparator(rounds, Team1, Team2):
    ATotal = 0
    BTotal = 0
    AScore = 0
    BScore = 0
    AHistory = []
    BHistory = []
    for i in xrange(rounds):
        AMove = Team1(i, BHistory, AHistory)
        BMove = Team2(i, AHistory, BHistory)
        if debug:
            print(AMove, BMove)
        if (AMove) and (BMove):
            AScore = AScore + 2
            AHistory.append(1)
            BScore = BScore + 2
            BHistory.append(1)
        if (AMove) and (not BMove):
            AScore = AScore + 0
            AHistory.append(1)
            BScore = BScore + 5
            BHistory.append(0)
        if (not AMove) and (BMove):
            AScore = AScore + 5
            AHistory.append(0)
            BScore = BScore + 0
            BHistory.append(1)
        if (not AMove) and (not BMove):
            AScore = AScore + 1
            AHistory.append(0)
            BScore = BScore + 1
            BHistory.append(0)
        ATotal+=AScore
        BTotal+=BScore
    return (ATotal, BTotal)

def go(rounds):
    TeamList=[x[0:-3] for x in os.listdir(os.curdir+'/uploads/PD') if x!='contest.py'
              and x[-3:]!='pyc' and x!='__init__.py' and x!='.DS_Store'
              and x[0]!='.']
    if debug:
        print TeamList
    TeamFunctions={}
    combinedArray={}

    sys.path.insert(0, './uploads/PD')
    for i in range(len(TeamList)):
        combinedArray[TeamList[i]]=0
    signal.signal(signal.SIGALRM, timeout_handler)
    toDelete=[]
    for teamNum in xrange(len(TeamList)):
        signal.alarm(0)
        try:
            new_module=__import__(TeamList[teamNum])
            new_module = reload(new_module)
            t = str(TeamList[teamNum])
            print 'imported '+str(TeamList[teamNum])
            signal.alarm(2)
            try:
                a = new_module.main(5,[0,0,0,0,0,0],[1,0,1,0,1,0])
            except TimeoutException:
                print 'Error code T'
                print 'Signal timed out'
                raise AssertionError
            except:
                print 'Error code 1'
                print 'Program failed to compile'
                raise AssertionError
            finally:
                signal.alarm(0)
            if a!=True and a!=False and a!=1 and a!=0:
                print 'Error code 2'
                print 'Function returned unexpected value'
                raise AssertionError
            else:
                TeamFunctions[t] = new_module.main
        except ImportError:
            try:
                t = str(''.join(list(TeamList[teamNum])[::1]))
                jfunc=(open('./uploads/PD/'+t+'.js','r')).read()
                trans = js2py.eval_js(jfunc)
                try:
                    signal.alarm(2)
                    try:
                        a = trans(5,[0,0,0,0,0,0],[1,0,1,0,1,0])
                    except:
                        print 'Error code 3'
                        print 'Signal timed out'
                        raise AssertionError
                    if a!=True and a!=False and a!=1 and a!=0:
                        print 'Error code 4'
                        print 'Function returned unexpected value'
                        print 'Function returned '+str(a)
                        raise AssertionError
                    else:
                        raise SeemsToWork
                except SeemsToWork:
                    TeamFunctions[str(t)] = trans
                finally:
                    signal.alarm(0)
                    del trans
            except AssertionError:
                toDelete.append(TeamList[teamNum])
        except:
            print 'Error code 6'
            print 'WTF'
            print('ignoring '+TeamList[teamNum])
            toDelete.append(TeamList[teamNum])
    for i in toDelete:
        TeamList.remove(i)
    #print TeamFunctions
    #print 'now going'
    #print len(TeamFunctions)
    #[f(1,[1,1],[1,0]) for f in TeamFunctions.values()]
    #print 'ended'
    #print TeamFunctions
    scoreArray=[0 for x in range(len(TeamList))]
    for foo in TeamList:
        team1 = TeamFunctions[foo]
        #print team1(0,[1],[1])
        for bar in TeamList:
            team2 = TeamFunctions[bar]
            if (foo == bar):
                break
            #if debug:
                #print("A match will now begin between "+foo+" and "+bar)
            matchScore = Comparator(rounds, team2, team1)
            if debug:
                print matchScore
            scoreArray[TeamList.index(foo)] += matchScore[1]
            scoreArray[TeamList.index(bar)] += matchScore[0]
    if debug:
        print('-----------------------Game-Over-----------------------')
        print('After ' + str(rounds) + " rounds, the scores are:")
    bestScore = 0
    bestScoreInd = 9999
    for p in xrange(len(TeamList)):
        if debug:
            print(TeamList[p] + " : " + str(scoreArray[p]))
        if (bestScore < scoreArray[p]):
            bestScore = scoreArray[p]
            #print(bestScore)
            bestScoreInd = p
            #print(bestScoreInd)
    print('The winner was: ' + TeamList[bestScoreInd])
    completeScore = zip(TeamList, scoreArray)
    completeScore = sorted(completeScore, key = lambda x: x[1], reverse = True)
    return (completeScore, toDelete)

if __name__=="__main__":
    go()
