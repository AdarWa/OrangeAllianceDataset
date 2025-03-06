import api
import utils

class Match:
    match_key = None
    red = {"robot1": None, "robot2":None}
    blue = {"robot1": None, "robot2":None}
    
    def __init__(self, match_key):
        self.match_key = match_key
        info = api.get_match_info(match_key)
        for team in info[0]["participants"]:
            team_match_key = team["match_participant_key"]
            num = team["team_key"]
            alliance = team_match_key[-2:][0]
            pos = team_match_key[-2:][1]
            if alliance == "R":
                self.red[f"robot{pos}"] = {"team":num}
            else:
                self.blue[f"robot{pos}"] = {"team": num}
        det = api.get_match_details(match_key)[0]
        self.blue["robot1"]["auto_park"] = det["blue"]["robot1Auto"] != "NONE"
        self.blue["robot2"]["auto_park"] = det["blue"]["robot2Auto"] != "NONE"
        self.red["robot1"]["auto_park"] = det["red"]["robot1Auto"] != "NONE"
        self.red["robot2"]["auto_park"] = det["red"]["robot2Auto"] != "NONE"
        
        self.blue["robot1"]["tele_ascent"] = det["blue"]["robot1Teleop"]
        self.blue["robot2"]["tele_ascent"] = det["blue"]["robot2Teleop"]
        self.red["robot1"]["tele_ascent"] = det["red"]["robot1Teleop"]
        self.red["robot2"]["tele_ascent"] = det["red"]["robot2Teleop"]
        
        self.blue["auto"] = {}
        self.blue["teleop"] = {}
        self.red["auto"] = {}
        self.red["teleop"] = {}
        
        self.blue["auto"]["sample_net"] = det["blue"]["autoSampleNet"]
        self.blue["auto"]["sample_low"] = det["blue"]["autoSampleLow"]
        self.blue["auto"]["sample_high"] = det["blue"]["autoSampleHigh"]
        self.blue["auto"]["specimen_low"] = det["blue"]["autoSpecimenLow"]
        self.blue["auto"]["specimen_high"] = det["blue"]["autoSpecimenHigh"]
        self.blue["teleop"]["sample_net"] = det["blue"]["teleopSampleNet"]
        self.blue["teleop"]["sample_low"] = det["blue"]["teleopSampleLow"]
        self.blue["teleop"]["sample_high"] = det["blue"]["teleopSampleHigh"]
        self.blue["teleop"]["specimen_low"] = det["blue"]["teleopSpecimenLow"]
        self.blue["teleop"]["specimen_high"] = det["blue"]["teleopSpecimenHigh"]
        
        self.red["auto"]["sample_net"] = det["red"]["autoSampleNet"]
        self.red["auto"]["sample_low"] = det["red"]["autoSampleLow"]
        self.red["auto"]["sample_high"] = det["red"]["autoSampleHigh"]
        self.red["auto"]["specimen_low"] = det["red"]["autoSpecimenLow"]
        self.red["auto"]["specimen_high"] = det["red"]["autoSpecimenHigh"]
        self.red["teleop"]["sample_net"] = det["red"]["teleopSampleNet"]
        self.red["teleop"]["sample_low"] = det["red"]["teleopSampleLow"]
        self.red["teleop"]["sample_high"] = det["red"]["teleopSampleHigh"]
        self.red["teleop"]["specimen_low"] = det["red"]["teleopSpecimenLow"]
        self.red["teleop"]["specimen_high"] = det["red"]["teleopSpecimenHigh"]
        
        self.blue["minor_fouls"] = det["blue"]["minorFouls"]
        self.blue["major_fouls"] = det["blue"]["majorFouls"]
        self.red["minor_fouls"] = det["red"]["minorFouls"]
        self.red["major_fouls"] = det["red"]["majorFouls"]
        
        self.blue["auto_points"] = det["blue"]["autoPoints"]
        self.red["auto_points"] = det["red"]["autoPoints"]
        
        self.blue["teleop_points"] = det["blue"]["teleopPoints"]
        self.red["teleop_points"] = det["red"]["teleopPoints"]
        
        self.blue["total_points"] = det["blue"]["preFoulTotal"]
        self.red["total_points"] = det["red"]["preFoulTotal"]

    def __str__(self):
        return f"Match {self.match_key}\nRed: {self.red}\nBlue: {self.blue}"

    def __repr__(self):
        return self.__str__()
        