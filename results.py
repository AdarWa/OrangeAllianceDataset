import api

class Results:
    team = ""
    rank = 0
    opr = 0
    wins = 0
    losses = 0
    ties = 0
    
    def __init__(self, json_data):
        import numpy as np
        if json_data:
            ranks = [data["rank"] for data in json_data]
            self.rank = np.mean(ranks)
            self.opr = max(data["np_opr"] for data in json_data)
            self.wins = sum(data["wins"] for data in json_data)
            self.losses = sum(data["losses"] for data in json_data)
            self.ties = sum(data["ties"] for data in json_data)
        self.team = json_data[0]["team"]["team_key"]
        awards = api.get_team_awards(self.team)
        print(f"Getting awards for team #{self.team}")
        if awards:
            min_award = min(awards, key=lambda x: x['award_rank'])
            self.award = min_award['award_name']
            self.award_rank = min_award['award_rank']
        else:
            self.award = "NONE"
            self.award_rank = 0
    def to_dict(self, include_team=False):
        if include_team:
            return {"team": self.team, "rank": self.rank, "opr": self.opr, "wins": self.wins, "losses": self.losses, "ties": self.ties, "award": self.award, "award_rank": self.award_rank}
        else:
            return {"rank": self.rank, "estimated_contribution_opr": self.opr, "wins": self.wins, "losses": self.losses, "ties": self.ties, "award": self.award, "award_rank": self.award_rank}
        