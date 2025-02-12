import requests
from datetime import datetime

teams = []

def get_teams_data():
    url = "https://theorangealliance.org/api/team?country=Israel"
    headers = {
        "X-TOA-Key": "jgSQw9EGUgss69BKfC1most39ZRbqVKI3BhUiH/OMGg=",
        "X-Application-Origin": "example.com"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        teams_data = response.json()
        return teams_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
def main():
    teams_data = get_teams_data()
    if teams_data:
        for team in teams_data:
            if team['last_active'] != "2425":
                continue
            t = {"number": team['team_number'], "name": team['team_name_short'], "seniority": datetime.now().year - team['rookie_year'], "has_website": team['website'] != ""}
            teams.append(t)
            print(t)

if __name__ == "__main__":
    main()