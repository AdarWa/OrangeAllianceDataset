import json
import api

if __name__ == "__main__":
    api.init("limiter")
    with open("selected_teams.json", "r") as f:
        teams = json.load(f)
        filtered_teams = [team for team in teams if team["country"] != "Israel"]
        print(f"Removed {len(teams) - len(filtered_teams)} teams from Israel")
        print(f"{len(filtered_teams)} teams remaining")
        israel_teams = api.get_teams_data("Israel")
        filtered_teams = israel_teams + filtered_teams
        print(f"Added {len(israel_teams)} teams from Israel")
        print(f"{len(filtered_teams)} teams total")
        filtered_teams = [team for team in filtered_teams if team["last_active"] == "2425"]
        print(f"Removed {len(filtered_teams) - len(filtered_teams)} teams that are not active in 2025")
        print(f"{len(filtered_teams)} teams remaining")
        with open("selected_teams.json", "w") as f:
            json.dump(filtered_teams, f, indent=4)
