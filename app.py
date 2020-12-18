from flask import Flask, render_template
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('lahmansbaseballdb.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM People WHERE nameFirst = "Alex" AND nameLast = "Rodriguez"').fetchall()
    return render_template('index.html', posts=posts)

@app.route('/arod')
def arod():
    conn = get_db_connection()
    matplotlib.use('agg')
    arodManager = conn.execute('SELECT yearID,teamID,lgID,W,L FROM People INNER JOIN Managers ON People.playerID=Managers.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()
    arodAllStar = conn.execute('SELECT YearID,teamID,lgID,startingPos FROM People INNER JOIN AllstarFull ON People.playerID=AllstarFull.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()

    arodBatting = conn.execute('SELECT yearID,Batting.R,Batting.H,Batting."2B",Batting."3B",Batting.HR FROM (People INNER JOIN Batting ON People.playerID = Batting.playerID) WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()
    avgBatting = conn.execute('SELECT yearID, AVG(Batting.R),AVG(Batting.H),AVG(Batting."2B"),AVG(Batting."3B"),AVG(Batting.HR) FROM Batting WHERE AB > 450 AND yearID IN (SELECT yearID FROM (People INNER JOIN Batting ON People.playerID = Batting.playerID) WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez") GROUP BY yearID').fetchall()
    avgBattingPD = pd.DataFrame(avgBatting)
    pdarodBatting = pd.DataFrame(arodBatting)
    cols = ['year runs hits 2B 3B HR']
    avgBattingPD.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    pdarodBatting.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    indexAROD = pdarodBatting['year'].tolist()

    dfHR = pd.DataFrame({'avgHR': avgBattingPD['HR'].tolist(), 'ARODHR':pdarodBatting['HR'].tolist()}, index=indexAROD)
    axHR = dfHR.plot.bar(rot=90, title="ARod HR VS Average Batter")
    figHR = axHR.get_figure()
    figHR.savefig('static/arodhr.jpg')

    dfRuns = pd.DataFrame({'avgRuns': avgBattingPD['runs'].tolist(), 'ARODRuns':pdarodBatting['runs'].tolist()}, index=indexAROD)
    axRuns = dfRuns.plot.bar(rot=90, title="ARod Runs VS Average Batter")
    figRuns = axRuns.get_figure()
    figRuns.savefig('static/arodruns.jpg')

    dfHits = pd.DataFrame({'avgHits': avgBattingPD['hits'].tolist(), 'ARODHits':pdarodBatting['hits'].tolist()}, index=indexAROD)
    axHits = dfHits.plot.bar(rot=90, title="ARod Hits VS Average Batter")
    figHits = axHits.get_figure()
    figHits.savefig('static/arodhits.jpg')

    df2B = pd.DataFrame({'avg2B': avgBattingPD['2B'].tolist(), 'AROD2B':pdarodBatting['2B'].tolist()}, index=indexAROD)
    ax2B = df2B.plot.bar(rot=90, title="ARod 2B VS Average Batter")
    fig2B = ax2B.get_figure()
    fig2B.savefig('static/arodsecb.jpg')

    df3B = pd.DataFrame({'avg3B': avgBattingPD['3B'].tolist(), 'AROD3B':pdarodBatting['3B'].tolist()}, index=indexAROD)
    ax3B = df3B.plot.bar(rot=90, title="ARod 3B VS Average Batter")
    fig3B = ax3B.get_figure()
    fig3B.savefig('static/arodthirb.jpg')

    arodFielding = conn.execute('SELECT yearID,teamID,Pos,G,A,E,ZR FROM People INNER JOIN Fielding ON People.playerID=Fielding.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()
    avgZoneR = conn.execute('SELECT yearID,AVG(ZR) FROM Fielding WHERE yearID in (SELECT yearID FROM People INNER JOIN Fielding ON People.playerID=Fielding.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez") GROUP BY yearID').fetchall()

    arodSalary = conn.execute('SELECT yearID, salary FROM People INNER JOIN Salaries ON People.playerID=Salaries.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()
    avgSalary = conn.execute('SELECT yearID, AVG(salary) FROM SALARIES WHERE yearID IN (SELECT yearID FROM People INNER JOIN Salaries ON People.playerID=Salaries.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez") GROUP BY yearID').fetchall()
    avgSalaryPD = pd.DataFrame(avgSalary)
    pdarodSalary = pd.DataFrame(arodSalary)
    cols = ['year salary']
    avgSalaryPD.rename(columns = {0:'year', 1:'salary'}, inplace = True)
    pdarodSalary.rename(columns = {0:'year', 1:'salary'}, inplace = True)
    indexARODSalary = pdarodSalary['year'].tolist()
    dfSalary = pd.DataFrame({'avgSalary': avgSalaryPD['salary'].tolist(), 'ARODSalary':pdarodSalary['salary'].tolist()}, index=indexARODSalary)
    axSalary = dfSalary.plot.bar(rot=90, title="ARod Salary VS Average MLB Salary")
    figSalary = axSalary.get_figure()
    figSalary.savefig('static/arodsalary.jpg')

    arodAwards = conn.execute('SELECT * FROM People INNER JOIN AwardsPlayers ON People.playerID=AwardsPlayers.playerID WHERE People.nameFirst = "Alex" AND People.nameLast = "Rodriguez"').fetchall()
    
    return render_template('arod.html', arodManager=arodManager,arodAllStar=arodAllStar,arodBatting=arodBatting,avgBatting=avgBatting,arodFielding=arodFielding,avgZoneR=avgZoneR,arodSalary=arodSalary,avgSalary=avgSalary,arodAwards=arodAwards)

@app.route('/altitude')
def altitude():
    return render_template('altitude.html')

@app.route('/peds')
def peds():
    return render_template('peds.html')

@app.route('/lookup')
def lookupPlayer():
    return render_template('lookup.html')