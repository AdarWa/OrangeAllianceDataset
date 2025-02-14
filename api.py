import utils
import requests_cache

s = None
KEY = utils.get_key()

def init():
    global s
    s = requests_cache.CachedSession('orange_cache')


def get_teams_data():
    url = "https://theorangealliance.org/api/team?country=Israel"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
    
    response = s.get(url, headers=headers)
    
    if response.status_code == 200:
        teams_data = response.json()
        return teams_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
def get_team_matches(team_number):
    url = f"https://theorangealliance.org/api/team/{team_number}/matches/2425"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
    
    response = s.get(url, headers=headers)
    
    if response.status_code == 200:
        matches_data = response.json()
        m = []
        for match in matches_data:
            m.append(match['match_key'])
        return m
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
def get_match_details(match_key):
    url = f"https://theorangealliance.org/api/match/{match_key}/details"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
        
    response = s.get(url, headers=headers)
        
    if response.status_code == 200:
        match_details = response.json()
        return match_details
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
def get_match_info(match_key):
    url = f"https://theorangealliance.org/api/match/{match_key}"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
        
    response = s.get(url, headers=headers)
        
    if response.status_code == 200:
        match_details = response.json()
        return match_details
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None