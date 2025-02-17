from match import Match

def get_key():
    with open('./secrets', 'r') as file:
        for line in file:
            if line.startswith('KEY='):
                return line.split('=', 1)[1].strip()
    print("No key found in secrets file")
    return None

def get_ascent_level(level):
    if level == "OBSERVATION_ZONE":
        return 1
    elif level == "NONE":
        return -1
    else:
        return int(level[-1:])
    
def get_points_from_ascent_level(level):
    if level == 1:
        return 3
    elif level == 2:    
        return 15
    elif level == 3:
        return 30
    elif level == -1:
        return 0
    else:
        return None
    
def get_team_data(team, match: Match):
    if match.red["robot1"]["team"] == team:
        return {"team": match.red["robot1"], "alliance": match.red}
    elif match.red["robot2"]["team"] == team:
        return {"team": match.red["robot2"], "alliance": match.red}
    elif match.blue["robot1"]["team"] == team:
        return {"team": match.blue["robot1"], "alliance": match.blue}
    elif match.blue["robot2"]["team"] == team:
        return {"team": match.blue["robot2"], "alliance": match.blue}
    else:
        return None