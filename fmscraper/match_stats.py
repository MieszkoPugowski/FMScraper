import requests
from bs4 import BeautifulSoup
import json
from fmscraper.xmas_generator import generate_xmas_header
from operator import itemgetter
import matplotlib as mpl
import matplotlib.pyplot as plt


class MatchStats:
    def __init__(self,match_id):
        self.url = "https://www.fotmob.com"
        self.id = match_id
        self.api_url = f'/api/data/matchDetails?matchId={self.id}'

    def get_json_content(self):
        headers = {
            "x-mas": generate_xmas_header(self.api_url)
        }
        full_url = self.url+self.api_url
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser').text
        data = json.loads(soup)
        return data