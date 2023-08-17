import logging
from pprint import pformat
from decscape.constants import *
from decscape.scraper import pull_all, pull_dec_file
from decscape.compiler import update, export


"""
{
    'Island': {
        'main': 45
        'side': 12
    }
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
