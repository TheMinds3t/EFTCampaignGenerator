from tkinter import BooleanVar
import json 


class ConfigSet:
    def __init__(self):
        self.tr_lvl_chances = [0.05,0.15,0.45]
        self.fence_allowed = False
        self.labs_only_dest = True

        # Overwrite default values with those in the file
        with open("config.json", "r") as confile:
            conf_file = json.load(confile)
            self.tr_lvl_chances = conf_file["trader_levels"]
            self.fence_allowed = conf_file["fence_allowed"]
            self.labs_only_dest = conf_file["labs_as_start"]
            confile.close()
    
    def saveconfig(self):
        with open("config.json", "w") as confile:
            out_format = {
                "trader_levels": self.tr_lvl_chances,
                "fence_allowed": self.fence_allowed,
                "labs_as_start": not self.labs_only_dest
            }
            confile.write(json.dumps(out_format, indent=4))
            confile.close()

configset = ConfigSet()