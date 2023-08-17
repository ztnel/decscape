import logging
from pprint import pformat
from decscape.constants import *
from decscape.scraper import pull_all, pull_dec_file
from decscape.compiler import update, export

"""
Deck Table
{
    cards: [
        id: 33423432
    ]
    date: 04/5/23,
}
"""
"""
Card Table
{
    'id': 3217839127,
    'name': 'Fatal Push',
    'counts': 45,
    'decks': 32,
    'main': 14,
    'side': 12,
    'trend': counts / decks * 4
}
"""
logging.basicConfig()
_log = logging.getLogger(__name__)
card_db: dict[str, dict[str, int]] = {}
buf = pull_all('https://www.mtgtop8.com/archetype?a=962&meta=191&f=PI')
# dec = pull_dec_file('https://www.mtgtop8.com/event?e=46783&d=545876&f=PI')
# formatting reference
"""
// FORMAT : Pioneer
1 [KTK] Dig Through Time
SB:  2 [] Sheoldred, the Apocalypse
"""
card_db = update(buf, card_db)
export(card_db)
# _log.info("%s", pformat(card_db))
