# -*- coding: utf-8 -*-
import os
import json
import logging
import argparse

from decscape.__version__ import __version__
from decscape.utils.logging import configure_logging
from decscape.constants import *
from decscape.scraper import pull_all
from decscape.compiler import update, export
from decscape.graph import plot, show

gpage = os.environ.get('PAGE', 'https://www.mtgtop8.com/archetype?a=808&meta=52&f=ST')
parser = argparse.ArgumentParser( prog='decscape', description='mtgtop8 web scraper', epilog='Text at the bottom of help')
parser.add_argument('-p', '--page')
parser.add_argument('-t', '--tclass', choices=['professional', 'major', 'competitive', 'open'])
args = parser.parse_args()

_logger = logging.getLogger(__name__)
configure_logging()
_logger.info("DecScape")
_logger.info("========")
_logger.info("Version: %s", __version__)

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

card_db: dict[str, dict[str, int]] = {}
_logger.info("Pulling decklists from: %s", gpage)
buf, deck_count, refs = pull_all(gpage, name="Temur Control")
# formatting reference
"""
// FORMAT : Pioneer
1 [KTK] Dig Through Time
SB:  2 [] Sheoldred, the Apocalypse
"""
card_db = update(buf, card_db, deck_count, refs)
export(card_db)
with open(EXPORT_PATH, 'r') as json_file:
    data_dict = json.load(json_file)
names = []
main_counts = []
side_counts = []
normalized_names = []
normalized_main_counts = []
normalized_side_counts = []
for card in data_dict.get("card_data"):
    names.append(card["name"])
    main_counts.append(card["main_counts"])
    side_counts.append(card["side_counts"])
    if card["name"] not in BASIC_KEYS:
        normalized_names.append(card["name"])
        normalized_main_counts.append(card["main_counts"] / deck_count)
        normalized_side_counts.append(card["side_counts"] / deck_count)

_logger.debug("names: %s", names)
_logger.debug("side_counts: %s", side_counts)
_logger.debug("main_counts: %s", main_counts)
_logger.debug("Normalized names: %s", normalized_names)
_logger.debug("Normalized side_counts: %s", normalized_side_counts)
_logger.debug("Normalized main_counts: %s", normalized_main_counts)

title_template = f'Cards in {deck_count} decks sampled from {gpage}' 
plot(names, main_counts, "Aggregate Mainboard " + title_template, 'Mainboard Counts', 'Card Name')
plot(names, side_counts,  "Aggregate Sideboard " + title_template, 'Sideboard Counts', 'Card Name')
plot(normalized_names, normalized_main_counts,'Normalized Mainboard ' + title_template, 'Mainboard Counts', 'Card Name')
plot(normalized_names, normalized_side_counts,'Normalized Sideboard '+ title_template, 'Sideboard Counts', 'Card Name')

show()

