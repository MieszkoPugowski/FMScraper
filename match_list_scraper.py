"""

Author: Mieszko Pugowski

FotMob scraper

**FOR EDUCATIONAL PURPOSES ONLY**
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setting up selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)


BASE_URL = "https://www.fotmob.com/leagues"
LEAGUE_ID = "38"
LEAGUE = "bundesliga"
SEASON = "2024-2025"
def pick_subsite(subsite):
    SUBSITES = ["table", "matches", "stats", "transfers", ]
    if subsite in SUBSITES:
        subsite_url = "/".join([BASE_URL, LEAGUE_ID, SUBSITES[SUBSITES.index(subsite)],
                                  LEAGUE])
        url_to_scrape = "?".join([subsite_url, f"season={SEASON}"])
        return url_to_scrape
    else:
        return f"Please pick correct subsite from: {SUBSITES}"


def consent_fotmob():
    wait = WebDriverWait(driver, 5)
    consent_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
    )
    consent_button.click()

def season_games_finder(url,rounds):
    games_list = []
    driver.get(url)
    consent_fotmob()
    for i in range(rounds):
        round_i = url +f"&group=by-round&round={i}"
        driver.get(round_i)
        try:
            time.sleep(2)
            hrefs = [a.get_attribute("href") for a in
                     driver.find_elements(By.CSS_SELECTOR,
                                          "a.css-1ajdexg-MatchWrapper.e1mxmq6p0")]
            if not hrefs:
                return "You have exceeded the number of rounds in the league"
            else:
                games_list.extend(hrefs)
        except:
            print(f"Error waiting for match {i}")
    driver.quit()
    return games_list

bundes_matches = season_games_finder(url=pick_subsite("matches"),rounds=32)
with open("games_list.txt","w") as file:
    for match in bundes_matches:
        file.write(f"{match}\n")

driver.quit()

