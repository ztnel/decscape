import re
import json
import logging
from decscape.constants import SIDEBOARD_PREFIX, LINE_REGEX, EXPORT_PATH

_logger = logging.getLogger(__name__)


def export(card_db: dict) -> None:
    with open(EXPORT_PATH, 'w') as fp:
        json.dump(card_db, fp, indent=4)
    _logger.info("Exported metadata to: %s", EXPORT_PATH)


def update(dec: str, card_db: dict, sample_size: int, refs: list[str]) -> dict:
    card_db["sample_size"] = sample_size
    card_db["refs"] = refs
    card_data = card_db["card_data"] = []
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
        # check existance
        if len(list(filter(lambda x: x["name"] == name, card_data))) == 0:
            card_data.append({"name": name, "main_counts": quantity if main else 0,
                             "side_counts": quantity if not main else 0})
        else:
            for card in card_data:
                if card["name"] == name:
                    if main:
                        card["main_counts"] += quantity
                    else:
                        card["side_counts"] += quantity
    return card_db
