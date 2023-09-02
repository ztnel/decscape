# -*- coding: utf-8 -*-
import json
import logging
import plotly.graph_objects as go
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

PAGE = 'https://www.mtgtop8.com/archetype?f=PI&meta=194&a=880'

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
buf = pull_all(PAGE)
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

fig = go.Figure()

# Create a horizontal bar chart for 'main' counts
fig.add_trace(go.Bar(y=names, x=main_counts, orientation='h', name='main', marker_color='blue'))

# Create a horizontal bar chart for 'side' counts
fig.add_trace(go.Bar(y=names, x=side_counts, orientation='h', name='side', marker_color='red'))

fig.update_layout(title_text="", yaxis_title="Card",
                  xaxis_title="Total Counts", barmode='group')
fig.show()
