
BASE_PATH = 'https://www.mtgtop8.com/'
EXPORT_FNAME = "data.json"
EXPORT_PATH = f"tmp/{EXPORT_FNAME}"
SIDEBOARD_PREFIX = 'SB:  '
LINE_REGEX = r'^(\d+)\s\[.*\]\s(.+)$'
DECK_LINK_REGEX = r'(event\?e=)(\d+)\&d=(\d+)&(.+)'

# Basic counts cannot be normalized since there is no limit on basics
BASIC_KEYS = ["Mountain", "Swamp", "Plains", "Island", "Forest"]
MAX_CARD_QUANTITY = 4

# tournament size filtering (by star icons)
TS_TD_CLASS="O16"