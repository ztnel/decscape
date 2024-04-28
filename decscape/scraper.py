import re
import logging
import requests
from enum import IntEnum
from bs4 import BeautifulSoup
from decscape.constants import BASE_PATH, DECK_LINK_REGEX, TS_TD_CLASS

_logger = logging.getLogger(__name__)

class TournamentClass(IntEnum):
    BIG_STAR = 0
    THREE_STARS=1
    TWO_STARS= 2
    ONE_STAR= 3


def pull_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    if soup.body is None:
        raise ValueError("No soup body found!")
    return soup


def get_tournament_class(tr) -> TournamentClass:
    tds = tr.find_all('td', class_=TS_TD_CLASS)
    _logger.info(tds)
    if tds.count('<img src="/graph/bigstar.png" height="20">'):
        return TournamentClass.BIG_STAR
    cnt = tds.count('<img src="/graph/star.png"/>')
    tclass = TournamentClass.ONE_STAR
    if (cnt == 1):
        tclass = TournamentClass.ONE_STAR
    elif (cnt == 2):
        tclass = TournamentClass.TWO_STARS
    elif (cnt == 3):
        tclass = TournamentClass.THREE_STARS
    return tclass

def pull_all(url: str, name:str|None=None, stars:str|None=None) -> tuple[str, int, list[str]]:
    soup = pull_soup(url)
    form = soup.find('form')
    if not form:
        raise
    deck_links = []
    for tr in form.find_all('tr', class_='hover_tr'):
        tclass = get_tournament_class(tr)
        arefs = tr.find_all('a')
        for aref in arefs:
            href = aref.get('href')
            match = re.match(DECK_LINK_REGEX, href)
            if match:
                # now perform filter by deck name if available
                if not name and not stars:
                    deck_links.append(f'{BASE_PATH}/{href}')
                elif not name:
                    deck_links.append(f'{BASE_PATH}/{href}')
                elif name in str(aref.text):
                    deck_links.append(f'{BASE_PATH}/{href}')
    count = len(deck_links)
    _logger.debug("Found decklist urls: %s", deck_links)
    _logger.info("Aggregating %s decklists", count)
    buffer = ""
    for dl in deck_links:
        buffer += pull_dec_file(dl)
    return buffer, count, deck_links


def pull_dec_file(url: str) -> str:
    """
    Pulls the .dec data from a deck page and returns the text buffer.
    """
    if '&d=' not in url:
        raise ValueError("invalid deck page")
    soup = pull_soup(url)
    aref = None
    link = soup.find(string='.dec')
    if link is None:
        raise ValueError()
    aref = link.find_parents("a")[-1].get('href')
    if aref is None:
        raise ValueError("No .dec link found")
    if 'd=' not in aref:
        raise ValueError("Invalid deck link")
    # .dec file
    r = requests.get(f'{BASE_PATH}/{aref}')
    return r.text
