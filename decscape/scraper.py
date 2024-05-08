import re
import json
import logging
import requests

from bs4 import BeautifulSoup, NavigableString
from datetime import datetime
from decscape.types import Deck, Metagame, TournamentClass, Format, Archetype
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

def get_metagame(format: Format) -> Metagame:
    """
    Scrape a metagame breakdown for a particular format
    """
    soup = pull_soup(f"{BASE_PATH}/format?f={format.value}")
    s14_divs = soup.find_all('div', class_="S14")
    if s14_divs is None:
        raise
    if isinstance(s14_divs, NavigableString):
        raise
    deck_sample_pattern = re.compile(r'^(\d.*) decks$')
    arch_percent_pattern = re.compile(r'^(\d.*) %$')
    samples = [int(deck_sample_pattern.match(s14_div.string).group(1)) for s14_div in s14_divs if s14_div.string is not None and re.match(deck_sample_pattern, s14_div.string)][-1] # type: ignore
    archetypes = []
    for arch_div in soup.find_all('div', class_="hover_tr", style="display:inline-block;width:48%;"):
        archetype_uri = arch_div.find('a').get('href')
        archetype_name = arch_div.find('a').string
        meta_share = [float(arch_percent_pattern.match(arch_subdiv.string).group(1)) for arch_subdiv in arch_div.find_all('div') if arch_subdiv.string is not None and re.match(arch_percent_pattern, arch_subdiv.string)][-1] # type: ignore
        archetypes.append(Archetype(archetype_name, f"{BASE_PATH}/{archetype_uri}", meta_share))
    return Metagame(format, samples, archetypes)

def pull_all(url: str, tclass:TournamentClass|None=None) -> tuple[str, int, list[str]]:
    entries = []
    soup = pull_soup(url)
    form = soup.find('form')
    if not form:
        raise
    for tr in form.find_all('tr', class_='hover_tr'):
        tds = tr.find_all('td')
        entry = Deck()
        day, month, year = str(tds[6].string).split('/')
        entry.date = datetime(int(year), int(month), int(day))
        entry.name = tds[1].find('a').string
        entry.uri = f"{BASE_PATH}/{tds[1].find('a').get('href')}"
        entry.player_uri = f"{BASE_PATH}/{tds[2].find('a').get('href')}"
        entry.tournament_uri = f"{BASE_PATH}/{tds[3].find('a').get('href')}"
        entry.tclass = get_tournament_class(tds[4])
        entries.append(entry)
    # apply name and tournament class filter
    tclass = TournamentClass.OPEN if tclass is None else tclass
    entries = list(filter(lambda x: x.tclass >= tclass, entries))
    count = len(entries)
    deck_links = [e.uri for e in entries]
    _logger.debug("Found decklist urls: %s", deck_links)
    _logger.info("Aggregating %s decklists", count)
    buffer = ""
    session = requests.Session()
    txt = []
    with session as s:
        for url in deck_links:
            if '&d=' not in url:
                _logger.warning("Bad url: %s skipping", url)
                continue
            r = s.get(url)
            txt.append(r.text)
    arefs = [get_dec_url(html) for html in txt]
    # .dec file
    with session as s:
        for aref in arefs:
            r = s.get(f'{BASE_PATH}/{aref}')
            buffer += r.text
    return buffer, count, deck_links

def get_dec_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.body is None:
        raise ValueError("No soup body found!")
    aref = None
    link = soup.find(string='.dec')
    if link is None:
        raise ValueError("Link not found")
    aref = link.find_parents("a")[-1].get('href')
    if aref is None:
        raise ValueError("No .dec link found")
    if 'd=' not in aref:
        raise ValueError("Invalid deck link")
    if not isinstance(aref, str):
        raise TypeError("Expected aref to be str")
    return aref

