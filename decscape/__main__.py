# -*- coding: utf-8 -*-
import json
import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from decscape.__version__ import __version__
from decscape.utils.logging import configure_logging
from decscape.constants import *
from decscape.scraper import pull_all
from decscape.compiler import update, export

_logger = logging.getLogger(__name__)
configure_logging()
_logger.info("DecScape")
_logger.info("=========================")
_logger.info("Version: %s", __version__)

PAGE = 'https://www.mtgtop8.com/archetype?f=PI&meta=193&a=888'

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
_logger.info("Pulling decklists from: %s", PAGE)
buf, deck_count = pull_all(PAGE, name="Boros Skalds")
# formatting reference
"""
// FORMAT : Pioneer
1 [KTK] Dig Through Time
SB:  2 [] Sheoldred, the Apocalypse
"""
card_db = update(buf, card_db)
export(card_db)
# Load data from a json file
with open(EXPORT_PATH, 'r') as json_file:
    data_dict = json.load(json_file)
names = list(data_dict.keys())
main_counts = [data_dict[name]['main'] for name in names]
side_counts = [data_dict[name]['side'] for name in names]
normalized_names = [key for key in data_dict.keys() if key not in BASIC_KEYS] 
normalized_main_counts = [data_dict[name]['main']/deck_count for name in names if name not in BASIC_KEYS]
normalized_side_counts = [data_dict[name]['side']/deck_count for name in names if name not in BASIC_KEYS]
#Creating subplot
fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Bar(y=names, x=main_counts, orientation='h', name='main', marker_color='blue'), row=1, col=1)
fig.add_trace(go.Bar(y=names, x=side_counts, orientation='h', name='side', marker_color='red'), row=1, col=1)

fig.add_trace(go.Bar(y=normalized_names, x=normalized_main_counts, orientation='h', name='main', marker_color='blue'), row=1, col=2)
fig.add_trace(go.Bar(y=normalized_names, x=normalized_side_counts, orientation='h', name='side', marker_color='red'), row=1, col=2)


fig.update_layout(barmode='group', legend=dict(x=0.5, y=1.1, orientation="h"))
fig.show()
