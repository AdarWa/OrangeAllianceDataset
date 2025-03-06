from match import Match

def get_key():
    with open('./secrets', 'r') as file:
        for line in file:
            if line.startswith('KEY='):
                return line.split('=', 1)[1].strip()
    print("No key found in secrets file")
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