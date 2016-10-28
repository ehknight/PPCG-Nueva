import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from tinydb import TinyDB, Query
from ast import literal_eval
from flask.ext.stormpath import StormpathManager,login_required, user

from uploads.PD.contest import go as contestMain
from random import randrange

app = Flask(__name__)
DEBUG = False

app.config['SECRET_KEY'] = 'pastaelephantgreenleafshoe'
app.config['STORMPATH_API_KEY_FILE'] = '~/.stormpath/apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'PPCG@Nueva'
app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True
stormpath_manager = StormpathManager(app)

app.config['UPLOAD_FOLDER'] = 'uploads/PD'
app.config['ALLOWED_EXTENSIONS'] = set(['py','js'])

teamsScores=[]
ignoreList=[]

prizeDB = TinyDB(os.curdir+'/databases/prizeDB.json')
previousChallengesDB = TinyDB(os.curdir+'/databases/previousChallengesDB.json')
Prize = Query()
Challenge = Query()

currentChallengeName="""Meta Tic-Tac-Toe"""

currentRules="""You must write a program to play the exciting game of meta tic-tac-toe! There are a couple of variations out there, but here is how we play it: We have a standard tic-tac-toe board but in each square there is another tic-tac-toe board. The turn flow works something like this:
<ol>
<li>If it is the first turn, Player 1 places an "O" in one of the squares in the center board. If not, Player 1 places an "O" in the board that coresponds to the square that Player 2 played in.</li>
<li>Player 2 then goes in the board corresponding to which square Player 1 played in. For example, if Player 1 goes in the top right square, Player 2 must play in the top right board.</li>
<li> Rinse and repeat until someone wins three boards in a row, similar to tic-tac-toe.</li>
</ol>
If a board is filled up, then you are directed to a random, non-filled up board. If that made no sense, visit <a href="https://s3.amazonaws.com/mpacampcashchallenge/UltimateTicTacToe.pdf">this</a> link to get a sense of what's going on, then read the rules again because there are some changes."""

currentTask="""
You must write a program meeting the requirements in the overarching
competition rules that plays meta tic-tac-toe. Your function
must take in parameters <tt>(teamNum, curState, activeBoardNum, wonBoards)</tt>, and be titled <tt>main</tt>. <tt>teamNum</tt> is either 1 or 0 and corresponds to "O" or "X". curState is the current state of the board, being a list of rows in a list of columns in a list of board rows in a list of board columns. So, if a game with a center board which has a 0 in the top-right corner of the center board were a curState, it would look like: <tt>[[[['','',''],['','',''],['','','']],[['','',''],['','',''],['','','']],[['','',''],['','',''],['','','']]],[[['','',''],['','',''],['','','']],[['','','0'],['','',''],['','','']],[['','',''],['','',''],['','','']]],[[[    '','',''],['','',''],['','','']],[['','',''],['','',''],['','','']],[['','',''],['',''    ,''],['','','']]]]</tt>. You could access that element by doing curState[1][1][0][2] (in English this translates to give me the second row of the board, then give me the second board of that, then give me the first row of the board, then give me the third column of that). activeBoardNum is a list of length 2. For example, if you were playing in the top-middle square, it activeBoardNum would be [0,1]. wonBoards is a 3x3 array of boards won. For example, if Player 0 has won the top left board it would look like <tt>[['0','',''],['','',''],['','','']]</tt>. Your function must return a list of length two of where you want to put your piece. For instance, if you want to go in the top right corner, you'd return <tt>[0,2]</tt>. Good luck and have fun!"""


@app.route('/')
def ayy():
    return render_template('index.html')

@app.route('/index.html')
def indexhtml():
    return render_template('index.html')

@app.route('/currentrules.html')
def currentruleshtml():
    return render_template('currentrules.html', currentTask=currentTask,
                           currentRules=currentRules,
                           currentChallengeName=currentChallengeName)

@app.route('/previous.html')
def previoushtml():
    return render_template('previous.html')

#code from http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def fileExt(filename):
    return filename.rsplit('.', 1)[1]

@login_required
@app.route('/submit.html')
def submithtml():
    return render_template('submit.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    print (str(user.given_name)+'just uploaded a new program!')
    file = request.files['file']
    checks = request.form.getlist('check')
    checked=False
    try:
        checks[0]
        checked=True
    except:
        pass
    if not checked:
        return render_template('submit.html', checked=checked)
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uniqueFilename= user.given_name+' '+user.surname+'.'+fileExt(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqueFilename))
        user.custom_data['programName'] = uniqueFilename
        return render_template('index.html', success=True)
    else:
        return render_template('index.html', success=False)

@app.route('/prizes.html')
def prizeshtml():
    t1=prizeDB.all()
    t2=[x['prize'] for x in t1]
    t3=[x['desc'] for x in t1]
    return render_template('prizes.html',
                           prizes=zip(t2,t3))

@app.route('/donate.html')
def donatehtml():
    return render_template('donate.html')

@app.route('/halloffame.html')
def halloffamehtml():
    scores=[('a',50),('b',100)]
    return render_template('halloffame.html', scores=teamsScores)

@app.route('/donateUpload', methods=['POST'])
def donateUpload():
    name = request.form['name']
    prize = request.form['prize']
    desc = request.form['description']
    email = request.form['email']
    prizeDB.insert({'name':name,'prize':prize,'desc':desc,'email':email})
    return render_template('index.html',uploadForm=True)

@app.route('/run')
def run():
    print 'running judge program'
    global teamsScores
    global ignoreList
    totalReturn=contestMain(20)
    teamsScores=totalReturn[0]
    ignoreList=totalReturn[1]
    return redirect('/leaderboard.html')

@app.route('/stupid.css')
def stupidcss():
    return render_template('stupid.css')

@app.route('/about.html')
def abouthtml():
    return render_template('about.html')

@app.route('/account')
@login_required
def accounthtml():
    try:
        tempPN = user.custom_data['programName']
    except KeyError:
        filesExt = [x for x in os.listdir(os.curdir+'/uploads/PD') if x!='contest.py'
                 and x[-3:]!='pyc' and x!='__init__.py' and x!='.DS_Store'
                 and x[0]!='.']
        files = [x[:-3] for x in filesExt]
        if (user.given_name+' '+user.surname) in files:
            user.custom_data['programName'] = ', '.join(
                [i for i in filesExt if (user.given_name+' '+user.surname) in i])
            tempPN = user.custom_data['programName']
        else:
            tempPN = 'No Program Submitted (yet!)'
    return render_template('account.html', name = user.given_name,
                           email = user.email,
                           programName =
                           tempPN)

@app.route('/leaderboard.html')
def leaderboardhtml():
    return render_template('leaderboard.html',scores=teamsScores,
                           ignoreLen = len(ignoreList), ignore=ignoreList)

@app.route('/favicon.ico')
def faviconico():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/png')

def archiveCurrentChallenge():
    prizeDB.insert({'name':currentChallengeName, 'task':currentTask,
                    'rules':currentRules})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80, debug=DEBUG, use_reloader=True)
