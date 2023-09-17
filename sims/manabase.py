
import coloredlogs
import random
import logging
from models.lands import *


# random.seed(1)

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger)
# number of iterations
epochs = 10000

# encode land sequencing
# NOTE: we cannot use a simple priority scheme due to complexities in conditional untapping for
# example consider a hand with 2x passade and Drowned Catacomb, we need to prioritize passage before
# drowned but then re-evaluate the priorities to play drowned before passage

# score?
# U -> 0.5
# B -> 0.5
U = 0
B = 0

deck = []


def restart_epoch():
    deck.clear()
    hand.clear()
    play.clear()
    deck.extend([DrownedCatacomb()] * 4)
    deck.extend([WateryGrave()] * 4)
    deck.extend([Island()] * 4)
    deck.extend([Swamp()] * 2)
    deck.extend([FieldOfRuin()] * 4)
    deck.extend([HiveOfTheEyeTyrant()] * 1)
    deck.extend([HallOfStormGiants()] * 1)
    deck.extend([ShipwreckMarsh()] * 1)
    deck.extend([Otawara()] * 1)
    deck.extend([FabledPassage()] * 2)
    deck.extend([NonLand()] * 36)
    random.shuffle(deck)


mulligan_count = 0
success_count = 0
fail_count = 0
play: list[Land] = []
hand = []
for i in range(epochs):
    restart_epoch()
    l1 = None
    l2 = None
    _logger.debug("Starting Epoch %s", i)
    # sample new hand
    for i in range(7):
        hand.append(deck.pop())
    _logger.debug("Hand: %s", ", ".join(str(card) for card in hand))
    lands = [card for card in hand if isinstance(card, Land)]
    # mull if under 2 lands
    land_count = len(lands)
    if land_count < 2:
        mulligan_count += 1
        _logger.warning("Mulligan due to insufficient lands")
        continue
    # we need minimum 1 colored land source (may succeed drawing 1 for turn)
    colored_lands = [l for l in lands if l.is_colored()]
    if len(colored_lands) < 1:
        fail_count += 1
        _logger.warning("Insufficient colored lands")
        continue
    basic_tapped_lands = [l for l in lands if l.is_tapped(play) and l.basic]
    tapped_lands = [l for l in lands if l.is_tapped(play)]
    if len(basic_tapped_lands) > 0:
        l1 = basic_tapped_lands[-1]
    elif len(tapped_lands) > 0:
        l1 = tapped_lands[-1]
    else:
        # take any colored untapped land
        l1 = [l for l in lands if not l.is_tapped(play) and l.is_colored()][-1]
    hand.remove(l1)
    play.append(l1)
    _logger.debug("Playing %s", play)
    # draw new card
    hand.append(deck.pop())
    lands = [card for card in hand if isinstance(card, Land)]
    _logger.debug("Hand: %s", ", ".join(str(card) for card in hand))
    untapped_lands = [l for l in lands if not l.is_tapped(play)]
    if sum(1 for land in untapped_lands if land.is_colored()) == 0:
        fail_count += 1
        _logger.warning("No more untapped colored lands for second land drop")
        continue
    if sum(1 for l in play if l.is_multicolored()) > 0:
        untapped_multicolor = [l for l in untapped_lands if l.is_colored()]
        l2 = untapped_multicolor[-1]
    elif sum(1 for l in play if l.blue) > 0:
        # look for untapped black
        untapped_black = [l for l in untapped_lands if l.black]
        if len(untapped_black) == 0:
            fail_count += 1
            _logger.warning("No more untapped black lands for second land drop")
            continue
        l2 = untapped_black[-1]
    elif sum(1 for l in play if l.black) > 0:
        # find untapped blue
        untapped_blue = [l for l in untapped_lands if l.blue]
        if len(untapped_blue) == 0:
            fail_count += 1
            _logger.warning("No more untapped blue lands for second land drop")
            continue
        l2 = untapped_blue[-1]
    else:
        raise RuntimeError("No blue or black mana in play on T2")
    hand.remove(l2)
    play.append(l2)
    _logger.debug("Playing %s", play)
    success_count += 1

_logger.info("---------------------------")
_logger.info("Success: %s", success_count)
_logger.info("Fail: %s", fail_count)
_logger.info("Mulligan: %s", mulligan_count)

result = int(U * 0.5 + B * 0.5 == 1)

# mulligan conditions: 1 or fewer lands
