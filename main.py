import api
import utils
from match import Match
import pandas as pd
import os
from results import Results
import random
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

teams = {}
teams_all_data = []
CHECKPOINT_FILE = "checkpoint.txt"

def read_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as file:
            return file.read().strip()
    return None

def write_checkpoint(team_num):
    with open(CHECKPOINT_FILE, "w") as file:
        file.write(team_num)

def process_match_data(team_num, match_key):
    try:
        match = Match(match_key)
        raw_data = utils.get_team_data(team_num, match)
        data = {}
        data["auto_park"] = raw_data["team"]["auto_park"]
        data["tele_ascent"] = raw_data["team"]["tele_ascent"]
        for i, auto in enumerate(raw_data["alliance"]["auto"]):
            data[f"auto_{auto}"] = raw_data["alliance"]["auto"][auto]
        for i, auto in enumerate(raw_data["alliance"]["teleop"]):
            data[f"teleop_{auto}"] = raw_data["alliance"]["teleop"][auto]
        data["minor_fouls"] = raw_data["alliance"]["minor_fouls"]
        data["major_fouls"] = raw_data["alliance"]["major_fouls"]
        data["auto_points"] = raw_data["alliance"]["auto_points"]
        data["teleop_points"] = raw_data["alliance"]["teleop_points"]
        return data
    except Exception as e:
        logging.error(f"Error processing match {match_key} for team {team_num}: {str(e)}")
        return None

def process_team(team):
    try:
        if team['last_active'] != "2425":
            return None
            
        t = {"number": team['team_number'], "name": team['team_name_short'], 
             "rookie_year": team['rookie_year'], "country": team['country'], 
             "has_website": team['website'] != ""}
        team_num = str(t["number"])
            
        matches = api.get_team_matches(team_num)
        if not matches or len(matches) == 0:
            logging.warning(f"No matches found for team #{team_num}")
            return None

        logging.info(f"Team #{team_num} {t['name']} started")
        teams[team_num] = {"details": t, "matches": []}
        
        valid_matches = []
        for match_key in matches:
            match_data = process_match_data(team_num, match_key)
            if match_data:
                valid_matches.append(match_data)
        
        if not valid_matches:
            logging.warning(f"No valid match data for team #{team_num}")
            return None
            
        teams[team_num]["matches"] = valid_matches
        
        df = pd.DataFrame(teams[team_num]["matches"])
        
        
        game_data = df.to_dict(orient="list")
        game_data = {key: ",".join(map(str, value)) for key, value in game_data.items()}
        team_data = teams[team_num]["details"]
        
        try:
            results = Results(api.get_team_results(team_num))
            results_dict = results.to_dict()
        except Exception as e:
            logging.error(f"Error getting results for team #{team_num}: {str(e)}")
            results_dict = {}
            
        all_data = {**team_data, **game_data, **results_dict}
        
        try:
            teams_data_df = pd.DataFrame([all_data])
            if not os.path.exists("data.csv"):
                headers = pd.DataFrame([all_data]).columns
                pd.DataFrame(columns=headers).to_csv("data.csv", index=True)
            teams_data_df.to_csv("data.csv", mode="a", header=False, index=True)
        except Exception as e:
            logging.error(f"Error saving data for team #{team_num}: {str(e)}")
        
        logging.info(f"Team #{team_num} {team_data['name']} done")
        write_checkpoint(team_num)
        
        return all_data
    except Exception as e:
        logging.error(f"Error processing team {team.get('team_number', 'unknown')}: {str(e)}")
        return None

def main():
    logging.info("Starting...")
    api.init('limiter')
    args = {}
    load_from_json = input("Load teams from JSON file? (y/n): ").strip().lower()
    if load_from_json == 'y':
        try:
            with open('selected_teams.json', 'r') as f:
                teams_data = json.load(f)
            print(f"Loaded {len(teams_data)} teams from selected_teams.json")
        except FileNotFoundError:
            print("selected_teams.json not found, proceed with API data")
            return
    else:
        while True:
            num_teams = input("Enter number of teams to process (leave blank for specific region): ").strip()
            try:
                args["num"] = int(num_teams)
                break
            except ValueError:
                pass
        if "num" not in args.keys():
            region = input("Enter region to process (leave blank for Israel): ").strip()
            args["region"] = region if region else "Israel"
        if args["num"]:
            regions = ['Israel', 'USA', 'Canada','Romania']
            selected_teams = []
            
            while len(selected_teams) < args["num"]:
                region = random.choice(regions)
                region_teams = api.get_teams_data(region)
                if region_teams:
                    available = [team for team in region_teams if team not in selected_teams]
                    num_needed = min(args["num"] - len(selected_teams), len(available))
                    selected_teams.extend(random.sample(available, num_needed))
                    
            selected_teams = [team for team in selected_teams if team['last_active'] == '2425']
            if len(selected_teams) < args["num"]:
                print(f"Warning: Only found {len(selected_teams)} active teams out of {args['num']} requested")
            
            teams_data = selected_teams[:args["num"]]
            
            with open('selected_teams.json', 'w') as f:
                json.dump(teams_data, f, indent=4)
            print(f"Saved {len(teams_data)} teams to selected_teams.json")
            return
        elif args["region"]:
            teams_data = api.get_teams_data(args["region"])
        else:
            teams_data = api.get_teams_data("Israel")
    
    
    last_processed_team = read_checkpoint()
    resume = True if last_processed_team is None else False
    
    if teams_data:
        print(f"Found {len(teams_data)} teams")
        for team in teams_data:
            if team['team_key'].strip() == last_processed_team:
                resume = True
                print(f"Resuming from team #{team['team_number']} {team['team_name_short']}")
                continue
            if resume:
                process_team(team)

if __name__ == "__main__":
    main()