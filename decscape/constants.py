
BASE_PATH = 'https://www.mtgtop8.com'
EXPORT_FNAME = "data.json"
EXPORT_PATH = f"tmp/{EXPORT_FNAME}"
SIDEBOARD_PREFIX = 'SB:  '
LINE_REGEX = r'^(\d+)\s\[.*\]\s(.+)$'

# Basic counts cannot be normalized since there is no limit on basics
BASIC_KEYS = ["Mountain", "Swamp", "Plains", "Island", "Forest"]
MAX_CARD_QUANTITY = 4
