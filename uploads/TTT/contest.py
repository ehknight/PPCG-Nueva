import random
from itertools import chain
import os, sys
import js2py
import signal

def testEntry(teamNum, curState, activeBoardNum, wonBoards):
    return False #ignore this

entries = {'entry1': testEntry} #ignore this


def printBoard(board):
    f = [['meme']]
    for bigRow in board:
        for bigColumn in bigRow:
            for row in bigColumn:
                tempRow = []
                for val in row[::1]:
                    if val == None:
                        tempRow.append(' ')
                    else:
                        tempRow.append(str(val))
                f.append(tempRow)
    for rowNum in range(28):
        if rowNum == 0:
            continue
        for valNum in range(3):
            if f[rowNum][valNum] == None:
                f[rowNum][valNum] = ' '
            f[rowNum][valNum] = str(f[rowNum][valNum])
    print([f[1], f[4], f[7]])
    print([f[2], f[5], f[8]])
    print([f[3], f[6], f[9]])
    print(['-----------------------------------------------'])
    print([f[10], f[13], f[16]])
    print([f[11], f[14], f[17]])
    print([f[12], f[15], f[18]])
    print(['-----------------------------------------------'])
    print([f[19], f[22], f[25]])
    print([f[20], f[23], f[26]])
    print([f[21], f[24], f[27]])

def won(*slots):
    """
    Checks if the slots are equal. 2 corresponds to both 0 and 1.
    """
    not2 = [x for x in slots if x!=2]
    notNoneLen = len([x for x in slots if x!=None])
    if notNoneLen != 3:
        return None
    if all(not2):
        return 1
    elif not any(not2):
        return 0
    else:
        return None

def checkWin(board):
    # first check rows
    wonList = []
    for row in board:
        wonList.append(won(*row))
    # now checks cols
    for col in zip(*board):
        wonList.append(won(*col))
    # check diags
    wonList.append(won(board[0][0], board[1][1], board[2][2]))
    wonList.append(won(board[0][0], board[1][1], board[2][2]))
    wonList.append(won(board[0][2], board[1][1], board[2][0]))
    if 1 in wonList and 0 in wonList:
        return 2
    notNone = [item for item in wonList if item != None]   
    if len(notNone)==0: return None
    assert all(e == notNone[0] for e in notNone) #check if all elems are equal
    return notNone[0]

def avaliableSpots(board, metaBoard):
    availSpots = [] #list of avaliable spots in meta-board
    for rowNum in range(len(metaBoard)):
        row = metaBoard[rowNum]
        for colNum in range(len(row)):
            if None in chain(*board[rowNum][colNum]):
                availSpots.append([rowNum, colNum])
    return availSpots

def playMove(funcs, teamNum, board, curBoard, metaBoard, debug=False):
    # funcs should be {0:[mainFunc, pickFunc]...}
    teamFunc = funcs[teamNum][0]
    otherTeamPick = funcs[abs(teamNum-1)][1] 
    try:
        move1 = teamFunc(teamNum, board, curBoard, metaBoard) # not move1
        if board[curBoard[0]][curBoard[1]][move1[0]][move1[1]] != None:
            raise AssertionError #trying to move in a taken square
        else:
            board[curBoard[0]][curBoard[1]][move1[0]][move1[1]] = teamNum
        for boardRow in range(3):
            for boardCol in range(3):
                won = checkWin(board[boardRow][boardCol])
                if won != None: #check to see if won small board
                    metaBoard[boardRow][boardCol] = won
        bigWon = checkWin(metaBoard) #check to see if won meta board
        if bigWon != None:
            return ["BigWin", bigWon, board, metaBoard]
        availSpots = avaliableSpots(board, metaBoard)
        if len(availSpots) == 0:
            return ["Draw", board, curBoard, metaBoard]
        elif move1 not in availSpots:
            curBoard = otherTeamPick(1, board, metaBoard)
            if curBoard not in availSpots:
                if debug:
                    print("Random Choice!!")
                curBoard = random.choice(availSpots)
        else:
            curBoard = move1
    except AssertionError:
        if debug:
            print("Invalid move; skipping turn.")
        pass
    return ["NoWin", board, curBoard, metaBoard]

def printTuple(tup):
    return "["+str(tup[0])+", "+str(tup[1])+"]"

def determineDrawWinner(metaBoard):
    ones = 0
    zeros = 0
    for row in metaBoard:
        for val in row:
            if val == 1:
                ones = ones + 1
            if val == 0:
                zeros = zeros + 1
    if ones > zeros:
        return 1
    if zeros > ones:
        return 0
    return None

def generateBlankBoard():
    return [[[[None, None, None] for _ in range(3)] for _ in range(3)]
             for _ in range(3)]

def generateMetaBoard():
    return [[None for _ in range(3)] for _ in range(3)]

def playMatch(rounds, team1, team1pick, team2, team2pick, debug=False):
    board = generateBlankBoard()
    # printBoard(board)
    metaBoard = generateMetaBoard()
    curBoard = [1, 1]
    funcs = {0:[team1, team1pick], 1:[team2, team2pick]}
    for turn in range(180):
        if debug:
            print("Current Board: "+printTuple(curBoard))
        winCode, board, curBoard, metaBoard = \
            playMove(funcs, 0, board, curBoard, metaBoard)
        if winCode == "BigWin":
            return board  # actually returning the winner
        elif winCode == "Draw":
            break
        if debug:
            printBoard(board)
            print("Current Board: "+printTuple(curBoard))
        winCode, board, curBoard, metaBoard = \
            playMove(funcs, 1, board, curBoard, metaBoard)
        if winCode == "BigWin":
            return board  # actually returning the winner
        elif winCode == "Draw":
            break        
        if debug:
            print("Round complete, here's the board:")
            printBoard(board)
            print(metaBoard[0])
            print(metaBoard[1])
            print(metaBoard[2])
    return None

def testMatch():
    def testFunc1(teamNum, board, curBoard, metaBoard):
        return eval(input("TEAM 0: What's your move, team " + str(teamNum) + "? "))
        
    def testFuncPick1(teamNum, board, metaBoard):
        return eval(input("TEAM 0: The opponent has picked a filled up square. Please "+
                     "pick a square that you'd like to play on."))
                     
    def testFunc2(teamNum, board, curBoard, metaBoard):
        return eval(input("TEAM 1: What's your move, team " + str(teamNum) + "? "))
    
    def testFuncPick2(teamNum, board, metaBoard):
        return eval(input("TEAM 1: The opponent has picked a filled up square. Please "+
                     "pick a square that you'd like to play on."))
    
    playMatch(testFunc1, testFuncPick1, testFunc2, testFuncPick2)

def playGame(rounds, team1, team1pick, team2, team2pick):
    teamTotals = [0, 0]
    for _ in range(rounds):
        match = playMatch(rounds, team1, team1pick, team2, team2pick)
        if match == None:
            continue
        teamTotals[match] += 1
    return teamTotals

def go(rounds, debug=False):
    class TimeoutException(Exception):   # Custom exception class
        pass
    
    class InitializationError(Exception):
        pass
    
    class PassThrough(Exception):
        pass
    
    def timeout_handler(signum, frame):   # Custom signal handler
        raise TimeoutException

    TeamList=[x[0:-3] for x in os.listdir(os.curdir+'/uploads/TTT') if x!='contest.py'
              and x[-3:]!='pyc' and x!='__init__.py' and x!='.DS_Store'
              and x[0]!='.']
    if debug:
        print(TeamList)
    TeamFunctions={}
    combinedArray={}
    defaultArgs = [0, generateBlankBoard(), [1,1], generateMetaBoard()]
    
    sys.path.insert(0, './uploads/TTT')
    for i in range(len(TeamList)):
        combinedArray[TeamList[i]]=0
    signal.signal(signal.SIGALRM, timeout_handler)
    toDelete=[]
    for teamNum in range(len(TeamList)):
        signal.alarm(0)
        try:
            new_module = __import__(TeamList[teamNum])
            t = str(TeamList[teamNum])
            print('imported '+str(TeamList[teamNum]))
            signal.alarm(1)
            try:
                a = new_module.main(*defaultArgs)
            except:
                print('Error code 1')
                print('Signal timed out')
                raise InitializationError
            finally:
                signal.alarm(0)
            try:
                if len(a)!=2:
                    raise InitializationError
            except:
                print('Error code 2')
                print('Function returned unexpected value')
                print('Function returned '+str(a))
                raise InitializationError
            else:
                TeamFunctions[t] = (new_module.main, new_module.pick)
        except ImportError:
            try:
                t = str(''.join(list(TeamList[teamNum])[::1]))
                jfunc=(open('./uploads/TTT/'+t+'.js','r')).read()
                ctx = execjs.compile(jfunc)
                trans = lambda *args: ctx.call("main", *args)
                transPick = lambda *args: ctx.call("pick", *args)
                try:
                    signal.alarm(2)
                    try:
                        a = trans(*defaultArgs)
                    except:
                        print('Error code 3')
                        print('Signal timed out')
                        raise InitializationError
                    try:
                        if len(a)!=2:
                            raise InitializationError
                    except:
                        print('Error code 4')
                        print('Function returned unexpected value')
                        print('Function returned '+str(a))
                        raise InitializationError
                    else:
                        raise PassThrough
                except PassThrough:
                    TeamFunctions[str(t)] = (trans, transPick)
                    continue
                finally:
                    signal.alarm(0)
                    del trans
                    del transPick
            except InitializationError:
                toDelete.append(TeamList[teamNum])
        except:
            print('Error code 6')
            print('WTF')
            print('ignoring '+TeamList[teamNum])
            toDelete.append(TeamList[teamNum])
    for i in toDelete:
        TeamList.remove(i)
    scoreArray=[0 for x in range(len(TeamList))]
    for _ in range(rounds):
        for foo in TeamList:
            team1, team1pick = TeamFunctions[foo]
            for bar in TeamList:
                team2, team2pick = TeamFunctions[bar]
                if (foo == bar):
                    break
                if debug:
                    print("A match will now begin between "+foo+" and "+bar)
                matchScore = playMatch(rounds, team1, team1pick, team2, team2pick)
                if debug:
                    print(matchScore)
                scoreArray[TeamList.index(foo)] += matchScore==0
                scoreArray[TeamList.index(bar)] += matchScore==1
    if debug:
        print('-----------------------Game-Over-----------------------')
        print('After ' + str(rounds) + " rounds, the scores are:")
    bestScore = 0
    print(scoreArray)
    bestScoreInd = 9999
    for p in range(len(TeamList)):
        if debug:
            print(TeamList[p] + " : " + str(scoreArray[p]))
        if (bestScore < scoreArray[p]):
            bestScore = scoreArray[p]
            #print(bestScore)
            bestScoreInd = p
            #print(bestScoreInd)
    try:
        print('The winner was: ' + TeamList[bestScoreInd])
    except IndexError:
        pass
    completeScore = zip(TeamList, scoreArray)
    completeScore = sorted(completeScore, key = lambda x: x[1], reverse = True)
    return (completeScore, toDelete)

if __name__=="__main__":
    go()
