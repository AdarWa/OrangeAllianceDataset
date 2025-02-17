import api
import filter_utils
import utils
from match import Match
import pandas as pd
import os
from results import Results

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

def main():
    api.init('limiter')    
    teams_data = api.get_teams_data("Israel")
    last_processed_team = read_checkpoint()
    resume = False if last_processed_team is None else True
    
    if teams_data:
        for team in teams_data:
            if team['last_active'] != "2425":
                continue
            t = {"number": team['team_number'], "name": team['team_name_short'], "seniority": 2025 - team['rookie_year'], "has_website": team['website'] != ""}
            team_num = str(t["number"])
            if resume:
                if team_num == last_processed_team:
                    resume = False
                continue
            matches = api.get_team_matches(team_num)
            if len(matches) == 0:
                continue
            print(f"Team #{team_num} {t['name']} started")
            teams[team_num] = {"details": t, "matches": []}
            for match_key in matches:
                match = Match(match_key)
                raw_data = utils.get_team_data(team_num,match)
                data = {}
                data["auto_park"] = 3 if raw_data["team"]["auto_park"] else 0
                data["tele_ascent"] = utils.get_points_from_ascent_level(raw_data["team"]["tele_ascent"])
                for i, auto in enumerate(raw_data["alliance"]["auto"]):
                    data[f"auto_{auto}"] = raw_data["alliance"]["auto"][auto]
                for i, auto in enumerate(raw_data["alliance"]["teleop"]):
                    data[f"teleop_{auto}"] = raw_data["alliance"]["teleop"][auto]
                data["foul_points"] = raw_data["alliance"]["foul_points"]
                data["auto_points"] = raw_data["alliance"]["auto_points"]
                data["teleop_points"] = raw_data["alliance"]["teleop_points"]
                data["total_points"] = raw_data["alliance"]["total_points"]
                teams[team_num]["matches"].append(data)
            
            total_points = [match["total_points"] for match in teams[team_num]["matches"]]
            estimated_contribution = filter_utils.estimate_contribution(total_points)
            teams[team_num]["details"]["estimated_contribution_minimize"] = estimated_contribution
            
            
            
            df = pd.DataFrame(teams[team_num]["matches"])
            
            auto_std = df["auto_points"].std()
            teleop_std = df["teleop_points"].std()

            min_std = 0 
            max_auto_std = df["auto_points"].max() - df["auto_points"].min()
            max_teleop_std = df["teleop_points"].max() - df["teleop_points"].min()

            teams[team_num]["details"]["auto_consistency"] = 1 - normalize_std(auto_std, min_std, max_auto_std)
            teams[team_num]["details"]["teleop_consistency"] = 1 - normalize_std(teleop_std, min_std, max_teleop_std)
            
            mean_tele_ascent = df["tele_ascent"].mean()
            std_tele_ascent = df["tele_ascent"].std()
            outlier_threshold = mean_tele_ascent + 2 * std_tele_ascent
            df["tele_ascent"] = df["tele_ascent"].apply(lambda x: mean_tele_ascent if x > outlier_threshold else x)
            
            game_data = df.mean().to_dict()
            team_data = teams[team_num]["details"]
            results = Results(api.get_team_results(team_num))
            results_dict = results.to_dict()
            all_data = {**team_data, **game_data, **results_dict}
            teams_all_data.append(all_data)
            teams_data_df = pd.DataFrame(teams_all_data)
            teams_data_df.to_csv("data.csv")
            print(f"Team #{team_num} {team_data["name"]} done")
            write_checkpoint(team_num)

def normalize_std(std, min_std, max_std):
    return (std - min_std) / (max_std - min_std)

if __name__ == "__main__":
    main()