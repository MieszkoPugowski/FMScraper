import requests
import json
from fmscraper.xmas_generator import generate_xmas_header
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import time


class FotMobStats:
    def __init__(self,league_id):
        self.url = "https://www.fotmob.com/api"
        self.league_id = league_id
        self.matchdetails_url = self.url+f'/matchDetails?matchId='
        self.leagues_url = self.url+f'/leagues?id={self.league_id}'
        self.team_url = self.url+f'/teams?id='
        self.player_url = self.url+f'/playerData?id='
        self.headers = {
            "x-mas": generate_xmas_header(self.matchdetails_url)
        }
        self.match_content_types = ['matchFacts', 'stats', 'playerStats',
                              'shotmap','lineup']

    def get_json_content(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


    def get_player_stats(self,player_id):


    def get_team_stats(self,team_id,tab):
        url = self.team_url+str(team_id)
        response = requests.get(url,headers=self.headers)
        response.raise_for_status()
        assert tab in response.json()
        return response.json()[tab]


    def get_season_stats(self,season_id,players_or_teams):
        if players_or_teams.lower() == "players":
            stats_url = f"https://www.fotmob.com/leagues/{self.league_id}/stats/season/{season_id}/players/accurate_long_balls"
        elif players_or_teams.lower() == "teams":
            stats_url = f"https://www.fotmob.com/leagues/{self.league_id}/stats/season/{season_id}/teams/accurate_cross_team"
        else:
            return "Please pick either 'teams' or 'players'"
        #selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(stats_url)
        wait = WebDriverWait(driver, 5)
        consent_button = wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
        )
        consent_button.click()
        wait = WebDriverWait(driver, 10)
        stat_element = wait.until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, "select.eoy2tw2"))
        )
        # why i only see 5 stats?
        dropdown = Select(stat_element[1])


    def get_match_details(self, match_id,content_type:str):
        data = self.get_json_content(url=self.matchdetails_url + str(match_id))
        assert content_type in self.match_content_types
        return data['content'][content_type]

    def get_available_teams(self, season):
        season_formatted = season.replace("-", "%2F")
        data = self.get_json_content(url=self.leagues_url + f"&season={season_formatted}&tab=overview&type=league")
        try:
            teams = data['table'][0]['data']['table']['all']
        except KeyError as e:
            teams = data['table'][0]['data']['tables'][2]['table']['xg']
        teams_dict = {team['name'].lower(): {"name": team['name'].replace(" ", "-").lower(),
                                             "id": team['id']} for team in teams}
        return teams_dict


if __name__ == "__main__":
    klasa = FotMobStats(league_id=38)
