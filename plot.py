import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import json
import datetime

START=datetime.date(year=2013, month=1, day=1)
END=datetime.date.today()

def trim(opening):
    if ":" in opening:
        opening = opening[:opening.find(":")]
    if "," in opening:
        opening = opening[:opening.find(",")]
    if " #" in opening:
        opening = opening[:opening.find(" #")]
    if " Accepted" in opening:
        opening = opening[:opening.find(" Accepted")]
    if " Declined" in opening:
        opening = opening[:opening.find(" Declined")]
    return opening

def strtodate(s):
    return datetime.date(year=int(s[:4]), month=int(s[5:7]), day=int(s[8:10]))

def readdata(filename):
    with open(filename) as f:
        mydata = json.load(f)
    data = {}
    for key in mydata:
        data[strtodate(key)] = mydata[key]
    return data

def getdates(data):
    dates = []
    for key in data:
        dates.append(key)
    dates.sort()
    return dates

def getopenings(data):
    openings = set()
    for key in data:
        for opening in data[key]:
            if opening == "traps":
                continue
            openings.add(opening)
    return openings

def getopeningstats(data, dates, opening_name):
    played = []
    whitescore = []
    for date in dates:
        played.append(0)
        whitescore.append(0)
        for opening in data[date]:
            if opening_name in opening:
                played[-1] += data[date][opening][0]
                whitescore[-1] += data[date][opening][1]
    return played, whitescore

def getgeneralstats(data, dates):
    played = []
    whitescore = []
    for date in dates:
        played.append(data[date]["games"][0])
        whitescore.append(data[date]["games"][1])
    return played, whitescore

def plotgeneralpopularity(played, dates, picname, start=datetime.date(year=2020, month=1, day=1), end=datetime.date(year=2021, month=1, day=1), show=False):
    datestoplot = []
    playedtoplot = []
    for i in range(len(dates)):
        if dates[i] >= start and dates[i] <= end:
            datestoplot.append(dates[i])
            playedtoplot.append(played[i])

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    """plt.axvline(x=datetime.date(year=2015, month=8, day=1), label='Marathon Tournaments', color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2015, month=10, day=24), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2016, month=10, day=22), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=1, day=8), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=4, day=16), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=8, day=13), color='green', linestyle='--', linewidth=1, alpha=0.5)"""
    plt.axvline(x=datetime.date(year=2020, month=4, day=18), color='purple', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=8, day=1), label='Marathon Tournaments', color='purple', linestyle='--', linewidth=1, alpha=0.5)

    plt.axvline(x=datetime.date(year=2020, month=3, day=11), label='Covid-19 becomes a pandemic', color='red', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=10, day=23), label='\"The Queen\'s Gambit\" is released', color='b', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=12, day=25), label='Christmas', color='g',
                linestyle='--', linewidth=1, alpha=0.5)
    ax.plot(datestoplot, playedtoplot)
    plt.title('Games played per day in 2020')
    #plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.savefig(picname, dpi=200)
    if show:
        plt.show()

def plotopening(opplayed, opwscore, dates, played, opening_name, picname, start=START, end=END, useweeks=False, usemonths=False, show=True):
    deadliness = []
    opfrac = []
    datesrelevant = []
    playedrelevant = []
    opplayedrelevant = []
    for i in range(len(dates)):
        if dates[i] < start or dates[i] > end:
            continue
        datesrelevant.append(dates[i])
        playedrelevant.append(played[i])
        opplayedrelevant.append(opplayed[i])
        opfrac.append(opplayed[i] / played[i] * 1000)
        if opplayed[i] > 0:
            deadliness.append(opwscore[i] / opplayed[i] * 100)
        else:
            deadliness.append(-1)

    deadlinesstoplot = []
    opfractoplot = []
    datestoplot = []
    opplayedtoplot = []
    if useweeks:
        j = 0
        while j + 7 < len(datesrelevant):
            datestoplot.append(datesrelevant[j+3])
            curdeadliness = 0
            curopfrac = 0
            curopplayed = 0
            for i in range(7):
                curdeadliness += deadliness[j] / 7
                curopfrac += opfrac[j] / 7
                curopplayed += opplayedrelevant[j] / 7
                j += 1
            deadlinesstoplot.append(curdeadliness)
            opfractoplot.append(curopfrac)
            opplayedtoplot.append(curopplayed)
    else:
        deadlinesstoplot = deadliness
        opfractoplot = opfrac
        datestoplot = datesrelevant
        opplayedtoplot = opplayedrelevant

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, opplayedtoplot)
    plt.title(opening_name + 's played per day')
    plt.savefig(picname+"PerDay.png", dpi=200)
    if show:
        plt.show()

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, opfractoplot)
    plt.title('Frequency of ' + opening_name + ', per 1000 games')
    plt.savefig(picname+"Freq.png", dpi=200)
    if show:
        plt.show()

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, deadlinesstoplot)
    plt.title(opening_name + ' win rate for white, \%')
    plt.axhline(y=50, color='r', linestyle='dashed')
    plt.savefig(picname+"WinRate.png", dpi=200)
    if show:
        plt.show()

def plotstaffordtraps(data, start=START, end=END, useweeks=True, show=False):
    dates = getdates(data)
    datesrelevant = []
    for date in dates:
        if date >= start and date <= end:
            datesrelevant.append(date)

    traps = [[], [], [], [], []]
    trapsscore = [[], [], [], [], []]
    for date in datesrelevant:
        for i in range(5):
            traps[i].append(data[date]['traps'][i][0])
            trapsscore[i].append(data[date]['traps'][i][1])

    trapstoplot = [[], [], [], [], []]
    scoretoplot = [[], [], [], [], []]
    datestoplot = []
    if useweeks:
        for k in range(5):
            j = 0
            while j + 7 < len(datesrelevant):
                if k == 0:
                    datestoplot.append(datesrelevant[j + 3])
                curtraps = 0
                curscore = 0
                for i in range(7):
                    curtraps += traps[k][j] / 7
                    curscore += trapsscore[k][j] / 7
                    j += 1
                trapstoplot[k].append(curtraps)
                scoretoplot[k].append(curscore)
    else:
        trapstoplot = traps
        scoretoplot = trapsscore
        datestoplot = datesrelevant

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, trapstoplot[0], label="Oh no, my queen")
    ax.plot(datestoplot, trapstoplot[1], label="Oh no, my knight")
    ax.plot(datestoplot, trapstoplot[2], label="5.e5 Ne4 6.d4 Qh4 7.g3 Ng3")
    ax.plot(datestoplot, trapstoplot[3], label="Punishing natural development")
    ax.plot(datestoplot, trapstoplot[4], label="Punishing hxg")
    plt.legend()
    plt.title('Stafford Gambit traps per day')
    plt.savefig("StaffordTraps.png", dpi=200)
    if show:
        plt.show()

def plotenglundtrap(data, start=START, end=END, useweeks=True, show=False):
    dates = getdates(data)
    datesrelevant = []
    for date in dates:
        if date >= start and date <= end:
            datesrelevant.append(date)

    traps = []
    trapsscore = []
    for date in datesrelevant:
        traps.append(data[date]['traps'][5][0])
        trapsscore.append(data[date]['traps'][5][1])

    trapstoplot = []
    scoretoplot = []
    datestoplot = []
    if useweeks:
        j = 0
        while j + 7 < len(datesrelevant):
            datestoplot.append(datesrelevant[j + 3])
            curtraps = 0
            curscore = 0
            for i in range(7):
                curtraps += traps[j] / 7
                curscore += trapsscore[j] / 7
                j += 1
            trapstoplot.append(curtraps)
            scoretoplot.append(curscore)
    else:
        trapstoplot = traps
        scoretoplot = trapsscore
        datestoplot = datesrelevant

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, trapstoplot)
    plt.title('Englund Gambit trap per day')
    plt.savefig("EnglundTrap.png", dpi=200)
    if show:
        plt.show()

if __name__ == "__main__":
    data = readdata('data')
    dates = getdates(data)

    #openings = getopenings(data)
    #print(len(openings))
    #shortopenings = {"Sicilian Defense"}
    #for opening in openings:
    #    shortopenings.add(trim(opening))
    #l = list(shortopenings)
    #l.sort()
    #print(l)
    #print(len(l))

    played, whitescore = getgeneralstats(data, dates)
    plotgeneralpopularity(played, dates, "TotalGames2020.png", show=True)

    #plotenglundtrap(data, datetime.date(year=2020, month=1, day=1), END, useweeks=False)
    #plotstaffordtraps(data, datetime.date(year=2020, month=1, day=1), END)

    #kindplayed, kindscore = getopeningstats(data, dates, "King's Indian")
    #plotopening(kindplayed, kindscore, dates, played, "King's Indian", "KingsIndian")

    #kgambitplayed, kgambitscore = getopeningstats(data, dates, "King's Gambit")
    #plotopening(kgambitplayed, kgambitscore, dates, played, "King's Gambit", "KingsGambit")

    #viennaplayed, viennascore = getopeningstats(data, dates, "Vienna")
    #plotopening(viennaplayed, viennascore, dates, played, "Vienna Game", "Vienna")

    #jalalplayed, jalalscore = getopeningstats(data, dates, "Jalalabad")
    #plotopening(jalalplayed, jalalscore, dates, played, "Sicilian Defense: Jalalabad Variation", "Jalalabad")

    #questplayed, questscore = getopeningstats(data, dates, "?")
    #plotopening(questplayed, questscore, dates, played, "?", "QuestionMark")

    #pinvarplayed, pinvarscore = getopeningstats(data, dates, "Sicilian Defense: Pin Variation")
    #plotopening(pinvarplayed, pinvarscore, dates, played, "Sicilian Defense: Pin Variation", "PinVariation")

    #englundplayed, englundscore = getopeningstats(data, dates, "Englund Gambit")
    #plotopening(englundplayed, englundscore, dates, played, "Englund Gambit", "Englund")

    #benkoplayed, benkoscore = getopeningstats(data, dates, "Benko Gambit")
    #plotopening(benkoplayed, benkoscore, dates, played, "Benko Gambit", "Benko")

    #benoniplayed, benoniscore = getopeningstats(data, dates, "Benoni Defense")
    #plotopening(benoniplayed, benoniscore, dates, played, "Benoni Defense", "Benoni")

    #qgaplayed, qgascore = getopeningstats(data, dates, "Queen's Gambit Accepted")
    #plotopening(qgaplayed, qgascore, dates, played, "Queen's Gambit Accepted", "QGA")

    #qgplayed, qgscore = getopeningstats(data, dates, "Queen's Gambit")
    #plotopening(qgplayed, qgscore, dates, played, "Queen's Gambit", "QG")

    #panovplayed, panovscore = getopeningstats(data, dates, "Panov Attack")
    #plotopening(panovplayed, panovscore, dates, played, "Caro-Kann Defense: Panov Attack", "Panov")

    #caroplayed, caroscore = getopeningstats(data, dates, "Caro-Kann Defense")
    #plotopening(caroplayed, caroscore, dates, played, "Caro-Kann Defense", "Caro-Kann")

    #schkostplayed, schkostscore = getopeningstats(data, dates, "Schilling-Kostic Gambit")
    #plotopening(schkostplayed, schkostscore, dates, played, "Schilling-Kostic Gambit", "Schilling-Kostic", useweeks=True)

    #twokfrenchplayed, twokfrenchscore = getopeningstats(data, dates, "French Defense: Two Knights Variation")
    #plotopening(twokfrenchplayed, twokfrenchscore, dates, played, "French Defense: Two Knights Variation", "TwoKnightsFrench", useweeks=True)

    #frenchplayed, frenchscore = getopeningstats(data, dates, "French Defense")
    #plotopening(frenchplayed, frenchscore, dates, played, "French Defense", "Frenchs", useweeks=True)

    #kveinisplayed, kveinisscore = getopeningstats(data, dates, "Sicilian Defense: Kveinis Variation")
    #plotopening(kveinisplayed, kveinisscore, dates, played, "Sicilian Defense: Kveinis Variation", "Kveinis", useweeks=True)

    #najdplayed, najdscore = getopeningstats(data, dates, "Sicilian Defense: Najdorf Variation")
    #plotopening(najdplayed, najdscore, dates, played, "Sicilian Defense: Najdorf Variation", "Najdorfs", useweeks=True)

    #adamsplayed, adamsscore = getopeningstats(data, dates, "Adams Attack")
    #plotopening(adamsplayed, adamsscore, dates, played, "Sicilian Defense: Najdorf Variation, Adams Attack", "Adams", useweeks=True)

    #staffplayed, staffscore = getopeningstats(data, dates, "Stafford Gambit")
    #plotopening(staffplayed, staffscore, dates, played, "Stafford Gambit", "Staffords", useweeks=True)

    #sicilianplayed, sicilianscore = getopeningstats(data, dates, "Sicilian Defense")
    #plotopening(sicilianplayed, sicilianscore, dates, played, "Sicilian Defense", "Sicilians", useweeks=True)

    #evansplayed, evansscore = getopeningstats(data, dates, "Evans Gambit")
    #plotopening(evansplayed, evansscore, dates, played, "Evans Gambit", "Evans", useweeks=True)

    #nakplayed, nakscore = getopeningstats(data, dates, "Italian Game: Scotch Gambit, Nakhmanson Gambit")
    #plotopening(nakplayed, nakscore, dates, played, "Nakhmanson Gambit", "Nakhmanson", useweeks=True)

    #gambitsplayed, gambitsscore = getopeningstats(data, dates, "Gambit")
    #plotopening(gambitsplayed, gambitsscore, dates, played, "Gambit", "Gambits", useweeks=True)