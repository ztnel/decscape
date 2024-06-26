# -*- coding: utf-8 -*-
import sys
from pprint import pprint
import json
import logging
import argparse

from dataclasses import asdict
from decscape.__version__ import __version__
from decscape.utils.logging import configure_logging
from decscape.constants import *
from decscape.scraper import pull_all, get_metagame
from decscape.compiler import update, export
from decscape.graph import plot, show
from decscape.types import Format

parser = argparse.ArgumentParser(prog='decscape', description='mtgtop8 web scraper', epilog='Text at the bottom of help')
parser.add_argument('-f', '--format', required=True, choices=list(Format), type=Format)
parser.add_argument('-a', '--archetype', type=str, default="")
parser.add_argument('-ga', '--get-archetypes', dest="ga", required=False, action='store_true')
parser.add_argument('-t', '--tclass', choices=['professional', 'major', 'competitive', 'open'], type=str, default="")
args = parser.parse_args()

_logger = logging.getLogger(__name__)
configure_logging()
_logger.info("DecScape")
_logger.info("========")
_logger.info("Version: %s", __version__)

metagame = get_metagame(args.format)
if args.ga:
    print(json.dumps([asdict(arch) for arch in metagame.archetypes], indent=4))
    sys.exit(1)
archetype_uri = next(filter(lambda x: True if args.archetype == "" else x.archetype_name == args.archetype, metagame.archetypes)).archetype_uri
if args.archetype == "":
    _logger.warning("Archetype not specified, extracting random archetype uri: %s", archetype_uri)
if archetype_uri is None:
    _logger.error("No archetype named: %s found. Referenced: %s", args.archetype, pprint(metagame.archetypes))
    sys.exit(1)

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
_logger.info("Pulling decklists from: %s", archetype_uri)
buf, deck_count, refs = pull_all(archetype_uri)
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

title_template = f'Cards in {deck_count} decks sampled from {archetype_uri}' 
plot(names, main_counts, "Aggregate Mainboard " + title_template, 'Mainboard Counts', 'Card Name')
plot(names, side_counts,  "Aggregate Sideboard " + title_template, 'Sideboard Counts', 'Card Name')
plot(normalized_names, normalized_main_counts,'Normalized Mainboard ' + title_template, 'Mainboard Counts', 'Card Name')
plot(normalized_names, normalized_side_counts,'Normalized Sideboard '+ title_template, 'Sideboard Counts', 'Card Name')

show()

