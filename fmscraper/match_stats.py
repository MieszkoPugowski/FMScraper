import requests
import json
from fmscraper.xmas_generator import generate_xmas_header


class MatchStats:
    def __init__(self,league_id):
        self.url = "https://www.fotmob.com/api"
        self.league_id = league_id
        self.matchdetails_url = self.url+f'/matchDetails?matchId='
        self.leagues_url = self.url+f'/leagues?id={self.league_id}'
        self.headers = {
            "x-mas": generate_xmas_header(self.matchdetails_url)
        }

    def get_json_content(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data

    def get_match_details(self, match_id):
        data = self.get_json_content(url=self.matchdetails_url + str(match_id))
        return data['content']

if __name__ == "__main__":
    klasa = MatchStats(league_id=38)
