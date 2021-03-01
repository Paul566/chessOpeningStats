import json, os
import chess.pgn

def read(filename, data):
    pgn = open(filename)
    cnt = 0
    while True:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)

        offset = pgn.tell()
        headers = chess.pgn.read_headers(pgn)
        if headers is None:
            break

        point = 0
        if headers['Result'] == '1-0':
            point = 1
        if headers['Result'] == '1/2-1/2':
            point = 0.5

        date = headers['UTCDate']
        if date not in data:
            data[date] = {}
            data[date]['games'] = [1, 0]
            data[date]['traps'] = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            """
            0: Oh no my queen, Stafford
            1: Oh no my knight, Stafford
            2: Stafford: 5.e5 Ne4 6.d4 Qh4 7.g3 Ng3
            3: Punishing natural development, Stafford
            4: Punishing capture hxg4, Stafford
            5: Englund gambit trap
            """
        else:
            data[date]['games'][0] += 1
        data[date]['games'][1] += point

        opening = headers["Opening"]
        if opening not in data[date]:
            data[date][opening] = [1, 0]
        else:
            data[date][opening][0] += 1
        data[date][opening][1] += point

        if opening == 'Englund Gambit' or opening == 'Russian Game: Stafford Gambit':
            pgn.seek(offset)
            mygame = chess.pgn.read_game(pgn)

            for i in range(10):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'rnbqk2r/ppp1Pppp/8/8/8/5N2/PPP1PbPP/RNBQKB1R w KQkq - 0 6':
                data[date]['traps'][5][0] += 1
                data[date]['traps'][5][1] += point
                print(date, data[date]['traps'])
            mygame = mygame.game()

            for i in range(13):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'r1bBk2r/ppp2ppp/2p5/2b5/4n3/3P4/PPP2PPP/RN1QKB1R b KQkq - 0 7':
                data[date]['traps'][0][0] += 1
                data[date]['traps'][0][1] += point
                print(date, data[date]['traps'])
            mygame = mygame.game()

            for i in range(12):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'r1bqk2r/ppp2ppp/2p5/2b1P3/4n3/3P4/PPP2PPP/RNBQKB1R w KQkq - 1 7':
                data[date]['traps'][1][0] += 1
                data[date]['traps'][1][1] += point
                print(date, data[date]['traps'])
            mygame = mygame.game()

            for i in range(14):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'r1b1kb1r/ppp2ppp/2p5/4P3/3P3q/6n1/PPP2P1P/RNBQKB1R w KQkq - 0 8':
                data[date]['traps'][2][0] += 1
                data[date]['traps'][2][1] += point
                print(date, data[date]['traps'])
            mygame = mygame.game()

            for i in range(16):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'r1b1k2r/ppp2ppp/2p5/2b5/2B1P2q/2N4P/PPPP1nP1/R1BQ1RK1 w kq - 0 9':
                data[date]['traps'][3][0] += 1
                data[date]['traps'][3][1] += point
                print(date, data[date]['traps'])
            mygame = mygame.game()

            for i in range(17):
                if mygame.next() != None:
                    mygame = mygame.next()
            if mygame.board().fen() == 'r1b1k2r/ppp2pp1/2p5/2b4p/3qP1P1/2N5/PPPPBPP1/R1BQ1RK1 b kq - 0 9' or \
                    mygame.board().fen() == 'r1b1k2r/ppp2pp1/2pq4/2b4p/4P1P1/3P4/PPP1BPP1/RNBQ1RK1 b kq - 0 9':
                data[date]['traps'][4][0] += 1
                data[date]['traps'][4][1] += point
                print(date, data[date]['traps'])

    return data


if __name__ == "__main__":
    with open('data') as f:
        data = json.load(f)
    for i in range(9):
        data = read("lichess_db_standard_rated_2013-0"+str(i+1)+".pgn", data)
    data = read("lichess_db_standard_rated_2013-10.pgn", data)
    data = read("lichess_db_standard_rated_2013-11.pgn", data)
    data = read("lichess_db_standard_rated_2013-12.pgn", data)
    with open('data', 'w') as f:
        json.dump(data, f)
