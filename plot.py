import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import datetime

START = datetime.date(year=2013, month=1, day=1)
END = datetime.date.today()
colors = ['red', 'green', 'blue', 'orange', 'purple']


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


def plotgeneralpopularity(played, dates, picname, start=START, end=END, show=False, logscale=True, grid=False):
    datestoplot = []
    playedtoplot = []
    for i in range(len(dates)):
        if dates[i] >= start and dates[i] <= end:
            datestoplot.append(dates[i])
            playedtoplot.append(played[i])

    plt.figure()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    plt.axvline(x=datetime.date(year=2015, month=8, day=1), label='Marathon Tournaments', color='green', linestyle='--',
                linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2015, month=10, day=24), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2016, month=10, day=22), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=1, day=8), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=4, day=16), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2017, month=8, day=13), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=4, day=18), color='green', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=8, day=1), color='green', linestyle='--', linewidth=1, alpha=0.5)

    plt.axvline(x=datetime.date(year=2020, month=3, day=11), label='Covid-19 becomes a pandemic', color='red',
                linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=datetime.date(year=2020, month=10, day=23), label='\"The Queen\'s Gambit\" is released', color='b',
                linestyle='--', linewidth=1, alpha=0.5)
    #plt.axvline(x=datetime.date(year=2020, month=12, day=25), label='Christmas', color='orange',
    #            linestyle='--', linewidth=1, alpha=0.5)
    ax.plot(datestoplot, playedtoplot)
    plt.title('Games played per day on lichess')
    if logscale:
        plt.yscale('log')
    if grid:
        plt.grid()
    plt.legend()
    plt.xlim(start, end)
    plt.savefig(picname, dpi=200)
    if show:
        plt.show()


def plotopening(opplayed, opwscore, dates, played, opening_name, picname,
                start=datetime.date(year=2016, month=1, day=1), end=END, useweeks=False,
                useblackwrate=False, show=False, lines=[], ratecorona=False):
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
            if useblackwrate:
                deadliness.append(100 - opwscore[i] / opplayed[i] * 100)
            else:
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
            datestoplot.append(datesrelevant[j + 3])
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
    plt.rc('legend', fontsize=6)
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, opplayedtoplot)
    plt.title(opening_name + 's played per day')
    for i in range(len(lines)):
        plt.axvline(x=lines[i][0], label=lines[i][1], color=colors[i], linestyle='--', linewidth=1)
    if len(lines) > 0:
        plt.legend()
    plt.xlim(start, end)
    plt.savefig(picname + "PerDay.png", dpi=200)
    if show:
        plt.show()

    plt.figure()
    plt.rc('legend', fontsize=6)
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, opfractoplot)
    plt.title('Frequency of the ' + opening_name + ', per 1000 games')
    for i in range(len(lines)):
        plt.axvline(x=lines[i][0], label=lines[i][1], color=colors[i], linestyle='--', linewidth=1)
    if len(lines) > 0:
        plt.legend()
    plt.xlim(start, end)
    plt.savefig(picname + "Freq.png", dpi=200)
    if show:
        plt.show()

    plt.figure()
    plt.rc('legend', fontsize=6)
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(datestoplot, deadlinesstoplot)
    if not useblackwrate:
        plt.title('The ' + opening_name + ' win rate for white, %')
    else:
        plt.title('The ' + opening_name + ' win rate for black, %')
    plt.axhline(y=50, color='r', linestyle='dashed')
    if ratecorona:
        plt.axvline(x=datetime.date(year=2020, month=3, day=11), label='Covid-19 becomes a pandemic', color='red',
                    linestyle='--', linewidth=1)
        plt.legend()
    plt.xlim(start, end)
    plt.savefig(picname + "WinRate.png", dpi=200)
    if show:
        plt.show()
    plt.close('all')


def plotstaffordtraps(data, start=START, end=END, useweeks=False, show=False):
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
    plt.close()


def plotenglundtrap(data, start=START, end=END, useweeks=False, show=False):
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

    played, whitescore = getgeneralstats(data, dates)
    plotenglundtrap(data, datetime.date(year=2020, month=1, day=1), END)
    plotstaffordtraps(data, datetime.date(year=2020, month=1, day=1), END)

    plotgeneralpopularity(played, dates, "TotalGames.png", logscale=True, grid=True)
    plotgeneralpopularity(played, dates, "TotalGames2020.png", start=datetime.date(year=2020, month=1, day=1),
                          logscale=False, grid=False)
    
    orthoschnappplayed, orthoschnappscore = getopeningstats(data, dates, "Orthoschnapp Gambit")
    plotopening(orthoschnappplayed, orthoschnappscore, dates, played, "Orthoschnapp Gambit", "Orthoschnapp",
                lines=[[datetime.date(year=2020, month=7, day=12),
                        'youtube video \"The Orthoschnapp Gambit: Winning in 10 moves\" \nby Eric Rosen (0.08M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=10, day=20),
                        'youtube video \"Surprising a Grandmaster in 4 Moves | Orthoschnapp Gambit\" \nby Eric Rosen (0.54M views as of 2021-03-07)']])
    plotopening(orthoschnappplayed, orthoschnappscore, dates, played, "Orthoschnapp Gambit", "Orthoschnapp2020",
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=7, day=12),
                        'youtube video \"The Orthoschnapp Gambit: Winning in 10 moves\" \nby Eric Rosen (0.08M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=10, day=20),
                        'youtube video \"Surprising a Grandmaster in 4 Moves | Orthoschnapp Gambit\" \nby Eric Rosen (0.54M views as of 2021-03-07)']])

    jeromeplayed, jeromescore = getopeningstats(data, dates, "Jerome Gambit")
    plotopening(jeromeplayed, jeromescore, dates, played, "Jerome Gambit", "Jerome",
                lines=[[datetime.date(year=2017, month=4, day=4),
                        'youtube video \"Practical Application of the Jerome Gambit\" \nby Chess School (0.03M views as of 2021-03-07)'],
                       [datetime.date(year=2017, month=4, day=5),
                        'youtube video \"Is Jerome Gambit Sound?\" \nby Chess School (0.02M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=5, day=28),
                        'youtube video \"How to win in Chess | The NEW UNBEATABLE Gambit\" \nby chessbrah (0.55M views as of 2021-03-07)']])
    plotopening(jeromeplayed, jeromescore, dates, played, "Jerome Gambit", "Jerome2020",
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2017, month=4, day=4),
                        'youtube video \"Practical Application of the Jerome Gambit\" \nby Chess School (0.03M views as of 2021-03-07)'],
                       [datetime.date(year=2017, month=4, day=5),
                        'youtube video \"Is Jerome Gambit Sound?\" \nby Chess School (0.02M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=5, day=28),
                        'youtube video \"How to win in Chess | The NEW UNBEATABLE Gambit\" \nby chessbrah (0.55M views as of 2021-03-07)']])

    schkostplayed, schkostscore = getopeningstats(data, dates, "Schilling-Kostic Gambit")
    plotopening(schkostplayed, schkostscore, dates, played, "Schilling-Kostic Gambit", "Schilling-Kostic",
                useblackwrate=True, lines=[[datetime.date(year=2020, month=8, day=27),
                                            'youtube video \"Don\'t Accept This Gambit!\" \nby Eric Rosen (0.71M views as of 2021-03-07)']])
    plotopening(schkostplayed, schkostscore, dates, played, "Schilling-Kostic Gambit", "Schilling-Kostic2020",
                useblackwrate=True, start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=8, day=27),
                        'youtube video \"Don\'t Accept This Gambit!\" \nby Eric Rosen (0.71M views as of 2021-03-07)']])

    kgambitplayed, kgambitscore = getopeningstats(data, dates, "King's Gambit")
    plotopening(kgambitplayed, kgambitscore, dates, played, "King's Gambit", "KingsGambit", ratecorona=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])
    plotopening(kgambitplayed, kgambitscore, dates, played, "King's Gambit", "KingsGambit2020",
                start=datetime.date(year=2020, month=1, day=1), ratecorona=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])

    viennaplayed, viennascore = getopeningstats(data, dates, "Vienna")
    plotopening(viennaplayed, viennascore, dates, played, "Vienna Game", "Vienna", ratecorona=True,
                lines=[[datetime.date(year=2020, month=10, day=23),
                        'youtube video \"WIN WITH 1. E4 | The Vienna Gambit & System | Chess Openings\" \nby GothamChess (0.73M views as of 2021-03-07)']]
                )
    plotopening(viennaplayed, viennascore, dates, played, "Vienna Game", "Vienna2020", ratecorona=True,
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=10, day=23),
                        'youtube video \"WIN WITH 1. E4 | The Vienna Gambit & System | Chess Openings\" \nby GothamChess (0.73M views as of 2021-03-07)']])

    jalalplayed, jalalscore = getopeningstats(data, dates, "Jalalabad")
    plotopening(jalalplayed, jalalscore, dates, played, "Sicilian Defense: Jalalabad Variation", "SicilianJalalabad",
                useblackwrate=True, lines=[[datetime.date(year=2020, month=10, day=31),
                                            'youtube video \"THE JALALABAD: A NEW CHESS WEAPON\" \nby GothamChess (0.23M views as of 2021-03-07)']])
    plotopening(jalalplayed, jalalscore, dates, played, "Sicilian Defense: Jalalabad Variation",
                "SicilianJalalabad2020", useblackwrate=True, start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=10, day=31),
                        'youtube video \"THE JALALABAD: A NEW CHESS WEAPON\" \nby GothamChess (0.23M views as of 2021-03-07)']]
                )

    questplayed, questscore = getopeningstats(data, dates, "?")
    plotopening(questplayed, questscore, dates, played, "?", "QuestionMark", useblackwrate=True)

    pinvarplayed, pinvarscore = getopeningstats(data, dates, "Sicilian Defense: Pin Variation")
    plotopening(pinvarplayed, pinvarscore, dates, played, "Sicilian Defense: Pin Variation", "SicilianPinVariation",
                useblackwrate=True)
    plotopening(pinvarplayed, pinvarscore, dates, played, "Sicilian Defense: Pin Variation", "SicilianPinVariation2020",
                useblackwrate=True, start=datetime.date(year=2020, month=1, day=1))

    englundplayed, englundscore = getopeningstats(data, dates, "Englund Gambit")
    plotopening(englundplayed, englundscore, dates, played, "Englund Gambit", "Englund", useblackwrate=True,
                ratecorona=True, lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic'],
                                        [datetime.date(year=2020, month=11, day=18),
                                         'youtube video \"EVERYONE falls for this NEW opening trap\" \nby Eric Rosen (1.2M views as of 2021-03-07)']])
    plotopening(englundplayed, englundscore, dates, played, "Englund Gambit", "Englund2020", useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1), ratecorona=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic'],
                       [datetime.date(year=2020, month=11, day=18),
                        'youtube video \"EVERYONE falls for this NEW opening trap\" \nby Eric Rosen (1.2M views as of 2021-03-07)']])

    benkoplayed, benkoscore = getopeningstats(data, dates, "Benko Gambit")
    plotopening(benkoplayed, benkoscore, dates, played, "Benko Gambit", "Benko", useblackwrate=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])
    plotopening(benkoplayed, benkoscore, dates, played, "Benko Gambit", "Benko2020", useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])

    benoniplayed, benoniscore = getopeningstats(data, dates, "Benoni Defense")
    plotopening(benoniplayed, benoniscore, dates, played, "Benoni Defense", "Benoni", useblackwrate=True)
    plotopening(benoniplayed, benoniscore, dates, played, "Benoni Defense", "Benoni2020", useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1))

    qgplayed, qgscore = getopeningstats(data, dates, "Queen's Gambit")
    plotopening(qgplayed, qgscore, dates, played, "Queen's Gambit", "QG", ratecorona=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic'],
                       [datetime.date(year=2020, month=10, day=23), '\"The Queen\'s Gambit\" is released']])
    plotopening(qgplayed, qgscore, dates, played, "Queen's Gambit", "QG2020", ratecorona=True,
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic'],
                       [datetime.date(year=2020, month=10, day=23), '\"The Queen\'s Gambit\" is released']])

    panovplayed, panovscore = getopeningstats(data, dates, "Panov Attack")
    plotopening(panovplayed, panovscore, dates, played, "Caro-Kann Defense: Panov Attack", "Caro-CannPanov")
    plotopening(panovplayed, panovscore, dates, played, "Caro-Kann Defense: Panov Attack", "Caro-CannPanov2020",
                start=datetime.date(year=2020, month=1, day=1))

    caroplayed, caroscore = getopeningstats(data, dates, "Caro-Kann Defense")
    plotopening(caroplayed, caroscore, dates, played, "Caro-Kann Defense", "Caro-Kann", useblackwrate=True,
                ratecorona=True)
    plotopening(caroplayed, caroscore, dates, played, "Caro-Kann Defense", "Caro-Kann2020", useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1), ratecorona=True)

    twokfrenchplayed, twokfrenchscore = getopeningstats(data, dates, "French Defense: Two Knights Variation")
    plotopening(twokfrenchplayed, twokfrenchscore, dates, played, "French Defense: Two Knights Variation",
                "FrenchTwoKnights", ratecorona=True)
    plotopening(twokfrenchplayed, twokfrenchscore, dates, played, "French Defense: Two Knights Variation",
                "FrenchTwoKnights2020", start=datetime.date(year=2020, month=1, day=1), ratecorona=True)

    frenchplayed, frenchscore = getopeningstats(data, dates, "French Defense")
    plotopening(frenchplayed, frenchscore, dates, played, "French Defense", "French", ratecorona=True,
                useblackwrate=True)
    plotopening(frenchplayed, frenchscore, dates, played, "French Defense", "French2020", ratecorona=True,
                useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1))

    kveinisplayed, kveinisscore = getopeningstats(data, dates, "Sicilian Defense: Kveinis Variation")
    plotopening(kveinisplayed, kveinisscore, dates, played, "Sicilian Defense: Kveinis Variation", "SicilianKveinis",
                useblackwrate=True)
    plotopening(kveinisplayed, kveinisscore, dates, played, "Sicilian Defense: Kveinis Variation",
                "SicilianKveinis2020",
                useblackwrate=True, start=datetime.date(year=2020, month=1, day=1))

    najdplayed, najdscore = getopeningstats(data, dates, "Sicilian Defense: Najdorf Variation")
    plotopening(najdplayed, najdscore, dates, played, "Sicilian Defense: Najdorf Variation", "SilicianNajdorf",
                useblackwrate=True, lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])
    plotopening(najdplayed, najdscore, dates, played, "Sicilian Defense: Najdorf Variation", "SilicianNajdorf2020",
                useblackwrate=True, start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])

    adamsplayed, adamsscore = getopeningstats(data, dates, "Adams Attack")
    plotopening(adamsplayed, adamsscore, dates, played, "Sicilian Defense: Najdorf Variation, Adams Attack",
                "SilicianAdams", lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])
    plotopening(adamsplayed, adamsscore, dates, played, "Sicilian Defense: Najdorf Variation, Adams Attack",
                "SilicianAdams2020", start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])

    staffplayed, staffscore = getopeningstats(data, dates, "Stafford Gambit")
    plotopening(staffplayed, staffscore, dates, played, "Stafford Gambit", "Stafford", useblackwrate=True,
                ratecorona=True,
                lines=[[datetime.date(year=2020, month=2, day=9),
                        'youtube video \"Stafford Gambit Accepted\" \nby thechesswebsite (0.38M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=3, day=27),
                        'youtube video \"Winning in 12 moves with the Stafford Gambit\" \nby Eric Rosen (0.24M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=8, day=1),
                        'youtube video \"Beating Everyone with the Same Opening Trap\" \nby Eric Rosen (3.0M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=8, day=4),
                        'youtube video \"The Trappiest Opening in Chess? | Win Quickly with the Stafford Gambit\" \nby Eric Rosen (0.76M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=10, day=11),
                        'youtube video \"Trapping a Grandmaster in 7 Moves | Stafford Gambit\" \nby Eric Rosen (1.0M views as of 2021-03-07)']]
                )
    plotopening(staffplayed, staffscore, dates, played, "Stafford Gambit", "Stafford2020", useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1), ratecorona=True,
                lines=[[datetime.date(year=2020, month=2, day=9),
                        'youtube video \"Stafford Gambit Accepted\" \nby thechesswebsite (0.38M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=3, day=27),
                        'youtube video \"Winning in 12 moves with the Stafford Gambit\" \nby Eric Rosen (0.24M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=8, day=1),
                        'youtube video \"Beating Everyone with the Same Opening Trap\" \nby Eric Rosen (3.0M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=8, day=4),
                        'youtube video \"The Trappiest Opening in Chess? | Win Quickly with the Stafford Gambit\" \nby Eric Rosen (0.76M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=10, day=11),
                        'youtube video \"Trapping a Grandmaster in 7 Moves | Stafford Gambit\" \nby Eric Rosen (1.0M views as of 2021-03-07)']]
                )

    sicilianplayed, sicilianscore = getopeningstats(data, dates, "Sicilian Defense")
    plotopening(sicilianplayed, sicilianscore, dates, played, "Sicilian Defense", "Sicilian", ratecorona=True,
                useblackwrate=True,
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])
    plotopening(sicilianplayed, sicilianscore, dates, played, "Sicilian Defense", "Sicilian2020", ratecorona=True,
                useblackwrate=True,
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=3, day=11), 'Covid-19 becomes a pandemic']])

    evansplayed, evansscore = getopeningstats(data, dates, "Evans Gambit")
    plotopening(evansplayed, evansscore, dates, played, "Evans Gambit", "Evans", ratecorona=True,
                lines=[[datetime.date(year=2020, month=8, day=25),
                        'youtube video \"Learn the Evans and Nakhmanson Gambit | 10-Minute Chess Openings\" \nby GothamChess (0.17M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=11, day=17),
                        'youtube video \"Learn The Ultimate Chess Opening || The Evans Gambit!\" \nby agadmator\'s Chess Channel (0.54M views as of 2021-03-07)']]
                )
    plotopening(evansplayed, evansscore, dates, played, "Evans Gambit", "Evans2020",
                start=datetime.date(year=2020, month=1, day=1), ratecorona=True,
                lines=[[datetime.date(year=2020, month=8, day=25),
                        'youtube video \"Learn the Evans and Nakhmanson Gambit | 10-Minute Chess Openings\" \nby GothamChess (0.17M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=11, day=17),
                        'youtube video \"Learn The Ultimate Chess Opening || The Evans Gambit!\" \nby agadmator\'s Chess Channel (0.54M views as of 2021-03-07)']]
                )

    nakplayed, nakscore = getopeningstats(data, dates, "Italian Game: Scotch Gambit, Nakhmanson Gambit")
    plotopening(nakplayed, nakscore, dates, played, "Nakhmanson Gambit", "Nakhmanson",
                lines=[[datetime.date(year=2020, month=5, day=4),
                        'youtube video \"The Most Aggressive Gambit You\'ve Never Heard Of | Nakhmanson Gambit\" \nby Jonathan Schrantz (0.17M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=6, day=14),
                        'youtube video \"Insanely Aggressive Nakhmanson Gambit\" \nby thechesswebsite (0.20M views as of 2021-03-07)']])
    plotopening(nakplayed, nakscore, dates, played, "Nakhmanson Gambit", "Nakhmanson2020",
                start=datetime.date(year=2020, month=1, day=1),
                lines=[[datetime.date(year=2020, month=5, day=4),
                        'youtube video \"The Most Aggressive Gambit You\'ve Never Heard Of | Nakhmanson Gambit\" \nby Jonathan Schrantz (0.17M views as of 2021-03-07)'],
                       [datetime.date(year=2020, month=6, day=14),
                        'youtube video \"Insanely Aggressive Nakhmanson Gambit\" \nby thechesswebsite (0.20M views as of 2021-03-07)']])


