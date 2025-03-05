import utils
import time
import logging


s = None
KEY = utils.get_key()

def init(requests_type='cache'):
    global s
    global sleep_sec
    if requests_type == 'cache':
        import requests_cache
        s = requests_cache.CachedSession('orange_cache')
    elif requests_type == 'limiter':
        from requests_ratelimiter import LimiterSession
        s = LimiterSession(per_minute=33)
    elif requests_type == 'normal':
        import requests
        s = requests.Session()
    else:
        raise ValueError("Invalid requests type, please choose from 'cache', 'limiter' or 'normal'")
        


def get_teams_data(country=None):
    try:
        url = "https://theorangealliance.org/api/team"
        if country:
            url = f"https://theorangealliance.org/api/team?country={country}"
        headers = {
            "X-TOA-Key": KEY,
            "X-Application-Origin": "example.com"
        }
        
        response = s.get(url, headers=headers)
        
        if response.status_code == 200:
            teams_data = response.json()
            for team in teams_data:
                team['country'] = country
            return teams_data
        else:
            logging.error(f"Failed to retrieve data: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error getting teams data for country {country}: {str(e)}")
        return None
    
    
def get_team_matches(team_number):
    try:
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
            logging.error(f"Failed to retrieve data: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error getting matches for team {team_number}: {str(e)}")
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
    
def get_team_results(team_number):
    url = f"https://theorangealliance.org/api/team/{team_number}/results/2425"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
            
    response = s.get(url, headers=headers)
            
    if response.status_code == 200:
        results_data = response.json()
        return results_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def get_team_awards(team_number):
    url = f"https://theorangealliance.org/api/team/{team_number}/awards/2425"
    headers = {
        "X-TOA-Key": KEY,
        "X-Application-Origin": "example.com"
    }
            
    response = s.get(url, headers=headers)
            
    if response.status_code == 200:
        results_data = response.json()
        awards = []
        for award in results_data:
            awards.append({"award_rank": award['award']['display_order'], "award_name": award['award_name']})
        return awards
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None