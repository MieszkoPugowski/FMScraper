"""

Author: Mieszko Pugowski

FotMob scraper

**FOR EDUCATIONAL PURPOSES ONLY**
"""

LEAGUE_ID = "38"
LEAGUE = "bundesliga"
SUBSITES = ["table","matches","stats","transfers",]
SEASON = "2025-2026"
BASE_URL = "https://www.fotmob.com/leagues"


def pick_subsite(subsite):
    if subsite in SUBSITES:
        subsite_url = "/".join([BASE_URL, LEAGUE_ID, SUBSITES[SUBSITES.index(subsite)],
                                  LEAGUE])
        url_to_scrape = "?=".join([subsite_url, SEASON])
        return url_to_scrape
    else:
        return f"Please pick correct subsite from: {SUBSITES}"


