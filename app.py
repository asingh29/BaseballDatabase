from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

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
    conn = get_db_connection()
    matplotlib.use('agg')
    # > 800ft, 6 teams
    highAltBatting = conn.execute('SELECT yearID,AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE (Teams.name = "Kansas City Royals" OR Teams.name = "Minnesota Twins" OR Teams.name = "Atlanta Braves" OR Teams.name = "Pittsburgh Pirates" OR Teams.name = "Arizona Diamondbacks" OR Teams.name = "Colorado Rockies") AND yearID > 2000 GROUP BY yearID').fetchall()
    # < 100ft, 9 teams
    lowAltBatting = conn.execute('SELECT yearID,AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE (Teams.name = "New York Yankees" OR Teams.name = "Tampa Bay Rays" OR Teams.name = "Houston Astros" OR Teams.name = "Oakland Athletics" OR Teams.name = "Miami Marlins" OR Teams.name = "New York Mets" OR Teams.name = "Philadelphia Phillies" OR Teams.name = "San Diego Padres" OR Teams.name = "San Francisco Giants") AND yearID > 2000 GROUP BY yearID').fetchall()
    avgBatting = conn.execute('SELECT yearID,AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE yearID > 2000 GROUP BY yearID').fetchall()
    avgBattingPD = pd.DataFrame(avgBatting)
    highAltBattingPD = pd.DataFrame(highAltBatting)
    lowAltBattingPD = pd.DataFrame(lowAltBatting)

    cols = ['year runs hits 2B 3B HR']

    avgBattingPD.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    highAltBattingPD.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    lowAltBattingPD.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    indexLowAlt = lowAltBattingPD['year'].tolist()
    indexHighAlt = highAltBattingPD['year'].tolist()


    dfRuns = pd.DataFrame({'avgRuns': avgBattingPD['runs'].tolist(), 'High Alt Runs':highAltBattingPD['runs'].tolist()}, index=indexHighAlt)
    axRuns = dfRuns.plot.bar(rot=90, title="High Alt Runs VS Average Batter")
    figRuns = axRuns.get_figure()
    figRuns.savefig('static/highaltruns.jpg')
    
    dfHits = pd.DataFrame({'avgHits': avgBattingPD['hits'].tolist(), 'High Alt Hits':highAltBattingPD['hits'].tolist()}, index=indexHighAlt)
    axHits = dfHits.plot.bar(rot=90, title="High Alt Hits VS Average Batter")
    figHits = axHits.get_figure()
    figHits.savefig('static/highalthits.jpg')

    df2B = pd.DataFrame({'avg2B': avgBattingPD['2B'].tolist(), 'High Alt 2B':highAltBattingPD['2B'].tolist()}, index=indexHighAlt)
    ax2B = df2B.plot.bar(rot=90, title="High Alt 2B VS Average Batter")
    fig2B = ax2B.get_figure()
    fig2B.savefig('static/highaltsecb.jpg')

    df3B = pd.DataFrame({'avg3B': avgBattingPD['3B'].tolist(), 'High Alt 3B':highAltBattingPD['3B'].tolist()}, index=indexHighAlt)
    ax3B = df3B.plot.bar(rot=90, title="High Alt 3B VS Average Batter")
    fig3B = ax3B.get_figure()
    fig3B.savefig('static/highaltthirb.jpg')

    dfHR = pd.DataFrame({'avgHR': avgBattingPD['HR'].tolist(), 'High Alt HR':highAltBattingPD['HR'].tolist()}, index=indexHighAlt)
    axHR = dfHR.plot.bar(rot=90, title="High Alt HR VS Average Batter")
    figHR = axHR.get_figure()
    figHR.savefig('static/highalthr.jpg')


    dfRunsl = pd.DataFrame({'avgRuns': avgBattingPD['runs'].tolist(), 'Low Alt Runs':lowAltBattingPD['runs'].tolist()}, index=indexLowAlt)
    axRunsl = dfRunsl.plot.bar(rot=90, title="Low Alt Runs VS Average Batter")
    figRunsl = axRunsl.get_figure()
    figRunsl.savefig('static/highaltrunsl.jpg')
    
    dfHitsl = pd.DataFrame({'avgHits': avgBattingPD['hits'].tolist(), 'Low Alt Hits':lowAltBattingPD['hits'].tolist()}, index=indexLowAlt)
    axHitsl = dfHitsl.plot.bar(rot=90, title="Low Alt Hits VS Average Batter")
    figHitsl = axHitsl.get_figure()
    figHitsl.savefig('static/highalthitsl.jpg')

    df2Bl = pd.DataFrame({'avg2B': avgBattingPD['2B'].tolist(), 'Low Alt 2B':lowAltBattingPD['2B'].tolist()}, index=indexLowAlt)
    ax2Bl = df2Bl.plot.bar(rot=90, title="Low Alt 2B VS Average Batter")
    fig2Bl = ax2Bl.get_figure()
    fig2Bl.savefig('static/highaltsecbl.jpg')

    df3Bl = pd.DataFrame({'avg3B': avgBattingPD['3B'].tolist(), 'Low Alt 3B':lowAltBattingPD['3B'].tolist()}, index=indexLowAlt)
    ax3Bl = df3Bl.plot.bar(rot=90, title="Low Alt 3B VS Average Batter")
    fig3Bl = ax3Bl.get_figure()
    fig3Bl.savefig('static/highaltthirbl.jpg')

    dfHRl = pd.DataFrame({'avgHR': avgBattingPD['HR'].tolist(), 'Low Alt HR':lowAltBattingPD['HR'].tolist()}, index=indexLowAlt)
    axHRl = dfHRl.plot.bar(rot=90, title="Low Alt HR VS Average Batter")
    figHRl = axHRl.get_figure()
    figHRl.savefig('static/highalthrl.jpg')

    return render_template('altitude.html')

@app.route('/peds')
def peds():
    conn = get_db_connection()
    matplotlib.use('agg')

    pre1975Batting = conn.execute('SELECT AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE yearID < 1975').fetchall()
    from75to90Batting = conn.execute('SELECT AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE yearID >= 1975 AND yearID < 1990').fetchall()
    from90to05Batting = conn.execute('SELECT AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE yearID >= 1990 AND yearID < 2005').fetchall()
    post2005Batting = conn.execute('SELECT AVG(Teams.R),AVG(Teams.H),AVG(Teams."2B"),AVG(Teams."3B"),AVG(Teams.HR) FROM (Teams) WHERE yearID >= 2005').fetchall()
    
    pre1975BattingPD = pd.DataFrame(pre1975Batting)
    from75to90BattingPD = pd.DataFrame(from75to90Batting)
    from90to05BattingPD = pd.DataFrame(from90to05Batting)
    post2005BattingPD = pd.DataFrame(post2005Batting)

    indexAROD = ["past-1974","1975-1989","1990-2004", "2005-now"]
    index = [0, 1, 2, 3]

    plt.clf()
    eraruns = [pre1975BattingPD[0].iloc[0], from75to90BattingPD[0].iloc[0], from90to05BattingPD[0].iloc[0], post2005BattingPD[0].iloc[0]]
    plt.bar(index, eraruns)
    plt.xlabel("ERAS")
    plt.ylabel("AVERAGE RUNS")
    plt.title("AVERAGE RUNS BY ERA")
    plt.xticks(index, indexAROD)
    plt.savefig('static/runsbyera.jpg')
    
    plt.clf()
    erahits = [pre1975BattingPD[1].iloc[0], from75to90BattingPD[1].iloc[0], from90to05BattingPD[1].iloc[0], post2005BattingPD[1].iloc[0]]
    plt.bar(index, erahits)
    plt.xlabel("ERAS")
    plt.ylabel("AVERAGE HITS")
    plt.title("AVERAGE HITS BY ERA")
    plt.xticks(index, indexAROD)
    plt.savefig('static/hitsbyera.jpg')
    
    plt.clf()
    eradoubles = [pre1975BattingPD[2].iloc[0], from75to90BattingPD[2].iloc[0], from90to05BattingPD[2].iloc[0], post2005BattingPD[2].iloc[0]]
    plt.bar(index, eradoubles)
    plt.xlabel("ERAS")
    plt.ylabel("AVERAGE DOUBLES")
    plt.title("AVERAGE DOUBLES BY ERA")
    plt.xticks(index, indexAROD)
    plt.savefig('static/doublesbyera.jpg')
    
    plt.clf()
    eratriples = [pre1975BattingPD[3].iloc[0], from75to90BattingPD[3].iloc[0], from90to05BattingPD[3].iloc[0], post2005BattingPD[3].iloc[0]]
    plt.bar(index, eratriples)
    plt.xlabel("ERAS")
    plt.ylabel("AVERAGE TRIPLES")
    plt.title("AVERAGE TRIPLES BY ERA")
    plt.xticks(index, indexAROD)
    plt.savefig('static/triplesbyera.jpg')
    
    plt.clf()
    erahomeruns = [pre1975BattingPD[4].iloc[0], from75to90BattingPD[4].iloc[0], from90to05BattingPD[4].iloc[0], post2005BattingPD[4].iloc[0]]
    plt.bar(index, erahomeruns)
    plt.xlabel("ERAS")
    plt.ylabel("AVERAGE HOME RUNS")
    plt.title("AVERAGE HOME RUNS BY ERA")
    plt.xticks(index, indexAROD)
    plt.savefig('static/homerunsbyera.jpg')
    plt.clf()
    return render_template('peds.html', pre1975Batting=pre1975Batting,from75to90Batting=from75to90Batting,from90to05Batting=from90to05Batting,post2005Batting=post2005Batting)

@app.route('/datascience')
def datascience():
    conn = get_db_connection()
    matplotlib.use('agg')

    Teams = conn.execute('select yearID,lgID,teamID,Teams.franchID,divID,G,Ghome,W,L,DivWin,WCWin,LgWin,WSWin,R,AB,H,"2B","3B",HR,BB,SO,SB,CS,HBP,SF,RA,ER,ERA,CG,SHO,SV,IPouts,HA,HRA,BBA,SOA,E,DP,FP,name,park,attendance,BPF,PPF,teamIDBR,teamIDlahman45,teamIDretro,TeamsFranchises.franchID,franchName,active,NAassoc from Teams inner join TeamsFranchises on Teams.franchID == TeamsFranchises.franchID where Teams.G >= 150 and TeamsFranchises.active == "Y"').fetchall()
    teams_df = pd.DataFrame(Teams)
    cols = ['yearID','lgID','teamID','franchID','divID','G','Ghome','W','L','DivWin','WCWin','LgWin','WSWin','R','AB','H','2B','3B','HR','BB','SO','SB','CS','HBP','SF','RA','ER','ERA','CG','SHO','SV','IPouts','HA','HRA','BBA','SOA','E','DP','FP','name','park','attendance','BPF','PPF','teamIDBR','teamIDlahman45','teamIDretro','franchID','franchName','active','NAassoc']
    teams_df.columns = cols
    drop_cols = ['lgID','franchID','divID','Ghome','L','DivWin','WCWin','LgWin','WSWin','SF','name','park','attendance','BPF','PPF','teamIDBR','teamIDlahman45','teamIDretro','franchID','franchName','active','NAassoc']
    df = teams_df.drop(drop_cols, axis=1)
    df = df.drop(['CS','HBP'], axis=1)
    df['SO'] = df['SO'].fillna(df['SO'].median())
    df['DP'] = df['DP'].fillna(df['DP'].median())
    matplotlib.pyplot.clf()
    matplotlib.pyplot.hist(df['W'])
    matplotlib.pyplot.xlabel('Wins')
    matplotlib.pyplot.title('Distribution of Wins')
    matplotlib.pyplot.savefig('static/winplot.jpg')
    matplotlib.pyplot.clf()

    def assign_win_bins(W):
        if W < 50:
            return 1
        if W >= 50 and W <= 69:
            return 2
        if W >= 70 and W <= 89:
            return 3
        if W >= 90 and W <= 109:
            return 4
        if W >= 110:
            return 5
    df['win_bins'] = df['W'].apply(assign_win_bins)
    matplotlib.pyplot.scatter(df['yearID'], df['W'], c=df['win_bins'])
    matplotlib.pyplot.title('Wins Scatter Plot')
    matplotlib.pyplot.xlabel('Year')
    matplotlib.pyplot.ylabel('Wins')
    matplotlib.pyplot.savefig('static/winscatter.jpg')
    matplotlib.pyplot.clf()

    df = df[df['yearID'] > 1900]
    runs_per_year = {}
    games_per_year = {}
    for i, row in df.iterrows():
        year = row['yearID']
        runs = row['R']
        games = row['G']
        if year in runs_per_year:
            runs_per_year[year] = runs_per_year[year] + runs
            games_per_year[year] = games_per_year[year] + games
        else:
            runs_per_year[year] = runs
            games_per_year[year] = games
    mlb_runs_per_game = {}
    for k, v in games_per_year.items():
        year = k
        games = v
        runs = runs_per_year[year]
        mlb_runs_per_game[year] = runs / games
    lists = sorted(mlb_runs_per_game.items())
    x, y = zip(*lists)
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.title('MLB Yearly Runs per Game')
    matplotlib.pyplot.xlabel('Year')
    matplotlib.pyplot.ylabel('MLB Runs per Game')
    matplotlib.pyplot.savefig('static/mlbyeaarlyruns.jpg')
    matplotlib.pyplot.clf()

    def assign_label(year):
        if year < 1920:
            return 1
        elif year >= 1920 and year <= 1941:
            return 2
        elif year >= 1942 and year <= 1945:
            return 3
        elif year >= 1946 and year <= 1962:
            return 4
        elif year >= 1963 and year <= 1976:
            return 5
        elif year >= 1977 and year <= 1992:
            return 6
        elif year >= 1993 and year <= 2009:
            return 7
        elif year >= 2010:
            return 8
    df['year_label'] = df['yearID'].apply(assign_label)
    dummy_df = pd.get_dummies(df['year_label'], prefix='era')
    df = pd.concat([df, dummy_df], axis=1)
    def assign_mlb_rpg(year):
        return mlb_runs_per_game[year]
    df['mlb_rpg'] = df['yearID'].apply(assign_mlb_rpg)

    def assign_decade(year):
        if year < 1920:
            return 1910
        elif year >= 1920 and year <= 1929:
            return 1920
        elif year >= 1930 and year <= 1939:
            return 1930
        elif year >= 1940 and year <= 1949:
            return 1940
        elif year >= 1950 and year <= 1959:
            return 1950
        elif year >= 1960 and year <= 1969:
            return 1960
        elif year >= 1970 and year <= 1979:
            return 1970
        elif year >= 1980 and year <= 1989:
            return 1980
        elif year >= 1990 and year <= 1999:
            return 1990
        elif year >= 2000 and year <= 2009:
            return 2000
        elif year >= 2010:
            return 2010
    df['decade_label'] = df['yearID'].apply(assign_decade)
    decade_df = pd.get_dummies(df['decade_label'], prefix='decade')
    df = pd.concat([df, decade_df], axis=1)
    df = df.drop(['yearID','year_label','decade_label'], axis=1)
    df['R_per_game'] = df['R'] / df['G']
    df['RA_per_game'] = df['RA'] / df['G']
    matplotlib.pyplot.scatter(df['R_per_game'], df['W'])
    matplotlib.pyplot.title('Runs per Game vs. Wins')
    matplotlib.pyplot.ylabel('Wins')
    matplotlib.pyplot.xlabel('Runs per Game')
    matplotlib.pyplot.savefig('static/runspergame.jpg')
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(df['RA_per_game'], df['W'])
    matplotlib.pyplot.title('Runs Allowed per Game vs. Wins')
    matplotlib.pyplot.xlabel('Runs Allowed per Game')
    matplotlib.pyplot.savefig('static/runsallowed.jpg')
    matplotlib.pyplot.clf()

    attributes = ['G','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','CG','SHO','SV','IPouts','HA','HRA','BBA','SOA','E','DP','FP','era_1','era_2','era_3','era_4','era_5','era_6','era_7','era_8','decade_1910','decade_1920','decade_1930','decade_1940','decade_1950','decade_1960','decade_1970','decade_1980','decade_1990','decade_2000','decade_2010','R_per_game','RA_per_game','mlb_rpg']
    data_attributes = df[attributes]
    s_score_dict = {}
    for i in range(2,11):
        km = KMeans(n_clusters=i, random_state=1)
        l = km.fit_predict(data_attributes)
        s_s = metrics.silhouette_score(data_attributes, l)
        s_score_dict[i] = [s_s]
    kmeans_model = KMeans(n_clusters=6, random_state=1)
    distances = kmeans_model.fit_transform(data_attributes)
    labels = kmeans_model.labels_
    matplotlib.pyplot.scatter(distances[:,0], distances[:,1], c=labels)
    matplotlib.pyplot.title('Kmeans Clusters')
    matplotlib.pyplot.savefig('static/kmeans.jpg')
    matplotlib.pyplot.clf()

    return render_template('datascience.html')

@app.route('/lookupteam')
def lookupTeam():
    return render_template('lookupteam.html')

@app.route('/lookupteam', methods=['POST'])
def lookupTeamStats():
    name = request.form['name']
    name = '\"' + name + '\"'
    year = request.form['year']
    conn = get_db_connection()
    getTeam = conn.execute('SELECT W,L,R,AB,H,"2B","3B",HR,BB,SO,SB,RA FROM Teams INNER JOIN TeamsFranchises ON Teams.franchID=TeamsFranchises.franchID WHERE TeamsFranchises.franchName = ' + name + ' AND Teams.yearID = ' + year).fetchall()
    avgTeam = conn.execute('SELECT AVG(W),AVG(L),AVG(R),AVG(AB),AVG(H),AVG("2B"),AVG("3B"),AVG(HR),AVG(BB),AVG(SO),AVG(SB),AVG(RA) FROM Teams INNER JOIN TeamsFranchises ON Teams.franchID=TeamsFranchises.franchID WHERE Teams.yearID = ' + year).fetchall()
    
    name = name[1:len(name)-1]
    return render_template('lookupteamsstats.html', getTeam=getTeam, name=name, year=year, avgTeam=avgTeam)

@app.route('/lookup')
def lookup():
    return render_template('lookup.html')

@app.route('/lookup', methods=['POST'])
def lookupplayer():
    name = request.form['name']
    print(name)
    names = name.split()
    firstName = '\"' + names[0] + '\"'
    lastName = '\"' + names[1] + '\"'

    conn = get_db_connection()
    matplotlib.use('agg')
    arodManager = conn.execute('SELECT yearID,teamID,lgID,W,L FROM People INNER JOIN Managers ON People.playerID=Managers.playerID WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName).fetchall()
    arodAllStar = conn.execute('SELECT YearID,teamID,lgID,startingPos FROM People INNER JOIN AllstarFull ON People.playerID=AllstarFull.playerID WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName).fetchall()

    arodBatting = conn.execute('SELECT yearID,Batting.R,Batting.H,Batting."2B",Batting."3B",Batting.HR FROM (People INNER JOIN Batting ON People.playerID = Batting.playerID) WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName).fetchall()
    avgBatting = conn.execute('SELECT yearID, AVG(Batting.R),AVG(Batting.H),AVG(Batting."2B"),AVG(Batting."3B"),AVG(Batting.HR) FROM Batting WHERE AB > 450 AND yearID IN (SELECT yearID FROM (People INNER JOIN Batting ON People.playerID = Batting.playerID) WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName + ') GROUP BY yearID').fetchall()
    avgBattingPD = pd.DataFrame(avgBatting)
    pdarodBatting = pd.DataFrame(arodBatting)
    cols = ['year runs hits 2B 3B HR']
    avgBattingPD.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    pdarodBatting.rename(columns = {0:'year', 1:'runs',
                                2:'hits', 3:'2B', 4:'3B', 5:'HR'}, inplace = True)
    indexAROD = pdarodBatting['year'].tolist()

    dfHR = pd.DataFrame({'avgHR': avgBattingPD['HR'].tolist(), 'PlayerHR':pdarodBatting['HR'].tolist()}, index=indexAROD)
    axHR = dfHR.plot.bar(rot=90, title= name + " HR VS Average Batter")
    figHR = axHR.get_figure()
    if os.path.exists("static/playerhr.jpg"):
        os.remove("static/playerhr.jpg")
    figHR.savefig('static/playerhr.jpg')

    dfRuns = pd.DataFrame({'avgRuns': avgBattingPD['runs'].tolist(), 'PlayerRuns':pdarodBatting['runs'].tolist()}, index=indexAROD)
    axRuns = dfRuns.plot.bar(rot=90, title= name + " Runs VS Average Batter")
    figRuns = axRuns.get_figure()
    if os.path.exists("static/playerruns.jpg"):
        os.remove("static/playerruns.jpg")
    figRuns.savefig('static/playerruns.jpg')

    dfHits = pd.DataFrame({'avgHits': avgBattingPD['hits'].tolist(), 'PlayerHits':pdarodBatting['hits'].tolist()}, index=indexAROD)
    axHits = dfHits.plot.bar(rot=90, title= name + " Hits VS Average Batter")
    figHits = axHits.get_figure()
    if os.path.exists("static/playerhits.jpg"):
        os.remove("static/playerhits.jpg")
    figHits.savefig('static/playerhits.jpg')

    df2B = pd.DataFrame({'avg2B': avgBattingPD['2B'].tolist(), 'Player2B':pdarodBatting['2B'].tolist()}, index=indexAROD)
    ax2B = df2B.plot.bar(rot=90, title= name + " 2B VS Average Batter")
    fig2B = ax2B.get_figure()
    if os.path.exists("static/playersecb.jpg"):
        os.remove("static/playersecb.jpg")
    fig2B.savefig('static/playersecb.jpg')

    df3B = pd.DataFrame({'avg3B': avgBattingPD['3B'].tolist(), 'Player3B':pdarodBatting['3B'].tolist()}, index=indexAROD)
    ax3B = df3B.plot.bar(rot=90, title= name + " 3B VS Average Batter")
    fig3B = ax3B.get_figure()
    if os.path.exists("static/playerthirb.jpg"):
        os.remove("static/playerthirb.jpg")
    fig3B.savefig('static/playerthirb.jpg')

    arodFielding = conn.execute('SELECT yearID,teamID,Pos,G,A,E,ZR FROM People INNER JOIN Fielding ON People.playerID=Fielding.playerID WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName).fetchall()
    avgZoneR = conn.execute('SELECT yearID,AVG(ZR) FROM Fielding WHERE yearID in (SELECT yearID FROM People INNER JOIN Fielding ON People.playerID=Fielding.playerID WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName + ') GROUP BY yearID').fetchall()

    arodAwards = conn.execute('SELECT * FROM People INNER JOIN AwardsPlayers ON People.playerID=AwardsPlayers.playerID WHERE People.nameFirst = ' + firstName + ' AND People.nameLast = ' + lastName).fetchall()
    
    return render_template('lookupplayer.html', arodManager=arodManager,arodAllStar=arodAllStar,arodBatting=arodBatting,avgBatting=avgBatting,arodFielding=arodFielding,avgZoneR=avgZoneR,arodAwards=arodAwards,name=name)