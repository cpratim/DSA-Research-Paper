import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import lxml

def get_player_stats(url, stype = 'per_game'):

    raw = requests.get(url).text
    soup = BeautifulSoup(raw, 'lxml')
    table = soup.find('table', {'id': stype})
    row2021 = table.find('tr', {'id': f'{stype}.2021'})
    row2022 = table.find('tr', {'id': f'{stype}.2022'})
    df = {'2021': {}, '2022': {}}
    for s in row2021.find_all('td'):
        df['2021'][s['data-stat']] = s.text

    for s in row2022.find_all('td'):
        df['2022'][s['data-stat']] = s.text
    return df

def get_box_score_urls(months = ['december', 'january', 'february', 'march', 'april', 'may', 'june', 'july']):

    base = 'https://www.basketball-reference.com/leagues/NBA_2021_games-{}.html'
    df = {}
    for m in months:
        df[m] = []
        raw = requests.get(base.format(m)).text
        soup = BeautifulSoup(raw, 'lxml')
        table = soup.find('table', {'id': 'schedule'})
        for tr in table.find('tbody').find_all('tr'):
            td = tr.find('td', {'data-stat': 'box_score_text'})
            try:
                url = td.find('a')['href']
            except:
                continue
            df[m].append(url)

    return df

def get_game_stats(urls):

    df = {}
    base = 'https://www.basketball-reference.com'
    for u in urls:
        match_id = u[-15:-5]
        df[match_id] = {'home': {}, 'away': {}}
        raw = requests.get(base + u).text
        soup = BeautifulSoup(raw, 'lxml')
        tables = soup.find_all('table')
        away_table, home_table = tables[0], tables[8]
        for td in away_table.find('tfoot').find('tr').find_all('td')[:-1]:
            df[match_id]['away'][td['data-stat']] = td.text
        for td in home_table.find('tfoot').find('tr').find_all('td')[:-1]:
            df[match_id]['home'][td['data-stat']] = td.text
    return df

def get_bulk_game_stats():
    df = get_box_score_urls()
    with open('data/matches_urls.json', 'w') as f:
        json.dump(df, f, indent = 4)
    with open('data/matches_urls.json', 'r') as f:
        d = json.load(f)
    urls = []
    for m in d:
        urls.extend(d[m])
    df = get_game_stats(urls)
    with open('data/game_stats.json', 'w') as f:
        json.dump(df, f, indent = 4)

def get_bulk_player_stats(stype = 'advanced'):
    with open('data/players.json', 'r') as f:
        players = json.load(f)

    df = {}
    for name, url in players.items():
        try:
            df[name] = get_player_stats(url, stype)
        except:
            continue
    with open('data/player_box.json', 'w') as f:
        json.dump(df, f, indent = 4)

if __name__ == '__main__':

    get_bulk_player_stats()


