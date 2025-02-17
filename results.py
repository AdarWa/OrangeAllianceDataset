import api

class Results:
    team = ""
    rank = 0
    opr = 0
    wins = 0
    losses = 0
    ties = 0
    
    def __init__(self, json_data):
        json_data = json_data[0]
        self.team = json_data["team"]["team_key"]
        self.rank = json_data["rank"]
        self.opr = json_data["np_opr"]
        self.wins = json_data["wins"]
        self.losses = json_data["losses"]
        self.ties = json_data["ties"]
        awards = api.get_team_awards(self.team)
        if awards:
            min_award = min(awards, key=lambda x: x['award_rank'])
            self.award = min_award['award_name']
        else:
            self.award = "NONE"
    
    def to_dict(self, include_team=False):
        if include_team:
            return {"team": self.team, "rank": self.rank, "opr": self.opr, "wins": self.wins, "losses": self.losses, "ties": self.ties, "award": self.award}
        else:
            return {"rank": self.rank, "estimated_contribution_opr": self.opr, "wins": self.wins, "losses": self.losses, "ties": self.ties, "award": self.award}
        