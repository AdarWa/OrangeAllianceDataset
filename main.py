import api
from match import Match

teams = {}


def main():
    api.init()
    TEAM = "19098"
    matches = api.get_team_matches(TEAM)
    total = []
    for match in matches:
        m = Match(match)
        if m.red["robot1"]["team"] == TEAM:
            total.append(m.red["total_points"])
        elif m.red["robot2"]["team"] == TEAM:
            total.append(m.red["total_points"])
        elif m.blue["robot1"]["team"] == TEAM:
            total.append(m.blue["total_points"])
        elif m.blue["robot2"]["team"] == TEAM:
            total.append(m.blue["total_points"])
    print(total)
    print(sum(total) / len(total))
        
    # teams_data = api.get_teams_data()
    # if teams_data:
    #     for team in teams_data:
    #         if team['last_active'] != "2425":
    #             continue
    #         t = {"number": team['team_number'], "name": team['team_name_short'], "seniority": 2025 - team['rookie_year'], "has_website": team['website'] != ""}
    #         matches = api.get_team_matches(t["number"])
    #         for match in matches:
    #             # print(match)
    #             print(api.get_match_details(match))
    #             break
    #         teams[t["number"]] = t
    #         print()
    #         break

if __name__ == "__main__":
    main()