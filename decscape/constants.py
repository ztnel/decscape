
BASE_PATH = 'https://www.mtgtop8.com/'
EXPORT_FNAME = "data.json"
EXPORT_PATH = f"tmp/{EXPORT_FNAME}"
SIDEBOARD_PREFIX = 'SB:  '
LINE_REGEX = r'^(\d+)\s\[.*\]\s(.+)$'
DECK_LINK_REGEX = r'(event\?e=)(\d+)\&d=(\d+)&(.+)'
