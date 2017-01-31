import bs4
import requests
import numpy as np
import time

def getFlatTable(score_url):
    res = requests.get(score_url)
    if '404' in res.url:
        raise Exception('No data found for this score')
    soup = bs4.BeautifulSoup(res.text)

    parsed = soup.findAll( 'div', 
            { 'class' : 'table_container', 'id' : 'div_games' }
            )
    rows = parsed[0].findAll('td')
    return rows

def unflattenTable(flat_soup):
    num_cols = 14
    table = [ flat_soup[i:i+num_cols] for i in range(0, len(flat_soup),num_cols) ]
    table = [ [j.get_text() for j in i ] for i in table ]
    return table

def loadScores(fname):
    s_table = np.genfromtxt(fname, delimiter=',').T
    scores = np.array([ s_table[2], s_table[3] ]).T
    numties = 0
    for i in scores:
        if i[0] == i[1]:
            numties += 1

    return scores, numties

if __name__=='__main__':
    url_base = 'http://www.pro-football-reference.com/boxscores/game_scores_find.cgi?pts_win={0}&pts_lose={1}' #Testing

    #here load array of scores with format [ [pt_win, pt_lose] ]...includes ties
    scores, ties = loadScores('./scores/scores2.txt') 
    #I want array of the form [ [pt_home, pt_away, counts] ]
    scores_fmt = np.zeros([2*len(scores) - ties, 3])
    
    k = 0
    for i in range(len(scores)):
        #time.sleep(5) #most likely not necessary, just in case they get suspicious ;)
        print k
        url = url_base.format( int(scores[i][0]), int(scores[i][1]) )
        flattable = getFlatTable(url)
        table = unflattenTable(flattable)
        if scores[i][0] == scores[i][1]: #ties
            scores_fmt[k][0], scores_fmt[k][1] = scores[i][0], scores[i][1]
            scores_fmt[k][2] += len(table)
            k+=1
        else: #wins/losses
            scores_fmt[k][0], scores_fmt[k][1] = scores[i][0], scores[i][1]
            scores_fmt[k+1][0], scores_fmt[k+1][1] = scores[i][1], scores[i][0]
            for j in table:
                if not j[5]: #home wins
                    scores_fmt[k][2] += 1
                else:
                    scores_fmt[k+1][2] += 1
            k+=2

    np.save('./scores/fmt_scores2.npy', scores_fmt)
