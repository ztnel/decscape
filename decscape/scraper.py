import logging
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from decscape.types import Entry, TournamentClass
from decscape.constants import BASE_PATH

_logger = logging.getLogger(__name__)

def pull_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    if soup.body is None:
        raise ValueError("No soup body found!")
    return soup

def get_tournament_class(tds) -> TournamentClass:
    imgs = tds.find_all('img')
    tclass = TournamentClass.MAJOR
    if (len(imgs) == 1):
        if (imgs[0].get('src') == '/graph/bigstar.png'):
            tclass = TournamentClass.PROFESSIONAL
        else:
            tclass = TournamentClass.OPEN
    elif (len(imgs) == 2):
        tclass = TournamentClass.COMPETITIVE
    elif (len(imgs) == 3):
        tclass = TournamentClass.MAJOR
    return tclass

def pull_all(url: str, name:str|None=None, tclass:TournamentClass|None=None) -> tuple[str, int, list[str]]:
    entries = []
    soup = pull_soup(url)
    form = soup.find('form')
    if not form:
        raise
    for tr in form.find_all('tr', class_='hover_tr'):
        tds = tr.find_all('td')
        entry = Entry()
        day, month, year = str(tds[6].string).split('/')
        entry.date = datetime(int(year), int(month), int(day))
        entry.deck_name = tds[1].find('a').string
        entry.deck_uri = f"{BASE_PATH}/{tds[1].find('a').get('href')}"
        entry.player_uri = f"{BASE_PATH}/{tds[2].find('a').get('href')}"
        entry.tournament_uri = f"{BASE_PATH}/{tds[3].find('a').get('href')}"
        entry.tclass = get_tournament_class(tds[4])
        entries.append(entry)
    # apply name and tournament class filter
    tclass = TournamentClass.OPEN if tclass is None else tclass
    entries = list(filter(lambda x: x.tclass > tclass, entries))
    entries = list(filter(lambda x: x.deck_name == name, entries))
    count = len(entries)
    deck_links = [e.deck_uri for e in entries]
    _logger.debug("Found decklist urls: %s", deck_links)
    _logger.info("Aggregating %s decklists", count)
    buffer = ""
    session = requests.Session()
    txt = []
    with session as s:
        for url in deck_links:
            if '&d=' not in url:
                continue
            r = s.get(url)
            txt.append(r.text)
    arefs = []
    for html in txt:
        arefs.append(pull_dec_file(html))
    # .dec file
    with session as s:
        for aref in arefs:
            r = s.get(f'{BASE_PATH}/{aref}')
            buffer += r.text
    return buffer, count, deck_links

def pull_dec_file(html: str) -> str:
    """
    Pulls the .dec data from a deck page and returns the text buffer.
    """
    soup = BeautifulSoup(html, "html.parser")
    if soup.body is None:
        raise ValueError("No soup body found!")
    aref = None
    link = soup.find(string='.dec')
    if link is None:
        raise ValueError()
    aref = link.find_parents("a")[-1].get('href')
    if aref is None:
        raise ValueError("No .dec link found")
    if 'd=' not in aref:
        raise ValueError("Invalid deck link")
    return aref

