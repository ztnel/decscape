import re
import json
import logging
from decscape.constants import SIDEBOARD_PREFIX, LINE_REGEX, EXPORT_PATH

_logger = logging.getLogger(__name__)


def export(card_db: dict) -> None:
    with open(EXPORT_PATH, 'w') as fp:
        json.dump(card_db, fp, indent=4)
    _logger.info("Exported metadata to: %s", EXPORT_PATH)


def update(dec: str, card_db: dict) -> dict:
    for line in dec.split('\n'):
        main = False
        if not line:
            continue
        if line[0].isdigit():
            main = True
        elif line.find(SIDEBOARD_PREFIX) != -1:
            line = line.lstrip(SIDEBOARD_PREFIX)
        else:
            continue
        match = re.match(LINE_REGEX, line)
        if match:
            quantity = int(match.group(1))  # returns '3'
            name = str(match.group(2)).rstrip()  # returns "Rona's Vortex"
        else:
            raise ValueError("Regex parse failed on classified input")
        meta = card_db.get(name)
        if meta is None:
            card_db[name] = {'side': 0, 'main': 0}
        if main:
            card_db[name]['main'] += quantity
        else:
            card_db[name]['side'] += quantity
    return card_db
