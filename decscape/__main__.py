import plotly.graph_objects as go
import logging
from pprint import pformat
from decscape.constants import *
from decscape.scraper import pull_all, pull_dec_file
from decscape.compiler import update, export
import json
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
buf = pull_all('https://www.mtgtop8.com/archetype?a=1543&meta=194&f=PI')
# dec = pull_dec_file('https://www.mtgtop8.com/event?e=46783&d=545876&f=PI')
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

fig.update_layout(title_text="Rakdos Sacrifice Card Distribution [13/08 - 15/08]", yaxis_title="Card",
                  xaxis_title="Total Counts", barmode='group')
fig.show()
