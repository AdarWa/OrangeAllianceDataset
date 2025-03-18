import api

class Results:
    team = ""
    rank = 0
    opr = 0
    wins = 0
    losses = 0
    ties = 0
    
    def __init__(self, json_data):
        if json_data:
            self.ranks = [data.get("rank",0) for data in json_data]
            self.opr = [data.get("np_opr",0) for data in json_data]
            self.wins = sum(data["wins"] for data in json_data)
            self.losses = sum(data["losses"] for data in json_data)
            self.ties = sum(data["ties"] for data in json_data)
        self.team = json_data[0]["team"]["team_key"]
        self.awards = [award["award_name"] for award in api.get_team_awards(self.team)]
        print(f"Getting awards for team #{self.team}")
        
    def to_dict(self, include_team=False):
        if include_team:
            return {"team": self.team, "rank": ",".join(map(str, self.ranks)), "estimated_contribution_opr": ",".join(map(str, self.opr)), "wins": self.wins, "losses": self.losses, "ties": self.ties, "awards": ",".join(self.awards)}
        else:
            return {"rank": ",".join(map(str, self.ranks)), "estimated_contribution_opr": ",".join(map(str, self.opr)), "wins": self.wins, "losses": self.losses, "ties": self.ties, "awards": ",".join(self.awards)}
        