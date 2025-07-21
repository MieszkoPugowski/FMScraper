import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept": "application/json, text/plain, */*",
    "x-mas": "eyJib2R5Ijp7InVybCI6Ii9hcGkvZGF0YS9tYXRjaERldGFpbHM/bWF0Y2hJZD00NTI1MzQxIiwiY29kZSI6MTc1MzA1MjE1ODg0NSwiZm9vIjoicHJvZHVjdGlvbjplNTkwMTg4ZTVjZWZkMTkyN2Y1OTcxNzAwYzVlODE3NWRiNzI5Mjg1LXVuZGVmaW5lZCJ9LCJzaWduYXR1cmUiOiI5NjA2MTgwMzBBMzJERDQ5QTlFQzY1QTY1Q0U4M0Q1NiJ9",

}


games_ids = []
with open("games_list.txt","r") as f:
    for line in f:
        match_id = line.split('#')[-1]
        games_ids.append(match_id.replace("\n",""))


API_URL = "https://www.fotmob.com/api/data/matchDetails?matchId="
for i in range(1):
    MATCH_ID = games_ids[i]
    new_url = API_URL + MATCH_ID
    response = requests.get(new_url, headers=HEADERS)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser').text
    data = json.loads(soup)
    content = data['content']
