# 
# Tarkov Campaign Generator - Console
# 
# Author: MINDS3T/Fire8TheBlade
# Concept: MINDS3T/Fire8TheBlade and Kharjaro
# 

import campaign_data as cd
import config 

import random 
import time

# Load and store the config data
configset = config.ConfigSet()

def gen_campaign():
    run_length = int(input("\nEnter the number of maps you'd like to traverse (between 2 to 6):\n\n > "))

    while run_length < 2 or run_length > 6:
        run_length = int(input("\n#####################################\n\nInvalid number. Enter the number of maps you'd like to traverse (between 2 to 6):\n\n > "))

    run_seed = input("\n#####################################\n\nEnter the seed, or leave blank for random:\n\n > ")

    if run_seed == "":
        random.seed(int(time.time()*1000)) 
        run_seed = random.randint(100000000,999999999)
    else:
        run_seed = int(run_seed)

    campaign = cd.Campaign(run_length,run_seed,trader_levels=configset.tr_lvl_chances,labs_final=configset.labs_only_dest,fence_allowed=configset.fence_allowed)
    path = campaign.full_path
    print("\n#####################################\n\nCampaign Seed =",run_seed)
    print("\nPrimary Objective for when you make it to "+campaign.end_map+": \n\t- "+campaign.mission_pri.replace("#","\n\t  "))
    print("\nSecondary Objective for all maps: \n\t- "+campaign.mission_sec.replace("#","\n\t  "))
    print("\nCampaign Path:\n")

    for i in range(0,len(path)):
        if i > 0:
            if campaign.trader_levels[i-1] > 1:
                print("\t = "+path[i] + " (" + campaign.trader_list[i-1] + " has stock available here, Levels 1-" + str(campaign.trader_levels[i-1]) + ")")
            else:
                print("\t = "+path[i] + " (" + campaign.trader_list[i-1] + " has stock available here, Level 1)")
        else:
            print("\t = "+path[i] + " (Start Here)")
        
        if i < len(path) - 1:
            print("\t.\n\t.\n\t.")

    print("\n#####################################")

def edit_config():
    mod_input = input("\nEnter the config value you'd like to change:\n1. Trader level chances\n2. Labs can be starting map\n3. Fence can be selected as trader\n4. Back to Main Menu\n\n > ")

    while not (mod_input == "1" or mod_input == "2" or mod_input == "3" or mod_input == "4"):
        mod_input = input("\nThat's an invalid option. Please enter the config value you'd like to change:\n1. Trader level chances\n2. Labs can be starting map\n3. Fence can be selected as trader\n4. Cancel Changes\n\n > ")

    print("\n#####################################")

    if mod_input == "1": # trader chances
        mod_input = input("\nThank you, now enter which trader level you'd like to change:\n1. Level 4 Chance ("+str(configset.tr_lvl_chances[0]*100)+
            "%)\n2. Level 3 Chance ("+str(configset.tr_lvl_chances[1]*100)
            +"%)\n3. Level 2 Chance ("+str(configset.tr_lvl_chances[2]*100)+"%)\n4. Cancel Changes\n\n > ")

        while not (mod_input == "1" or mod_input == "2" or mod_input == "3" or mod_input == "4"):
            mod_input = input("\n\nThat's not a valid option. Please enter which trader level you'd like to change:\n1. Level 4 Chance ("+str(configset.tr_lvl_chances[0]*100)+
            "%)\n2. Level 3 Chance ("+str(configset.tr_lvl_chances[1]*100)
            +"%)\n3. Level 2 Chance ("+str(configset.tr_lvl_chances[2]*100)+"%)\n4. Cancel Changes\n\n > ")

        if int(mod_input) == 4:
            print("\n#####################################\n\nChanges to the config cancelled!\n\n#####################################")
            return False

        trader_level = int(mod_input)-1
        chance = input("\nEnter a new chance threshold for trader level "+str(4 - trader_level)+" (100 = Every time), or enter 'h' for more information or 'c' to cancel changes:\n\n > ")
        break_flag = False

        while not break_flag:
            while not (chance.isdigit() or chance == "h" or chance == "c"):
                chance = input("\nPlease enter a new chance threshold for trader level "+str(4 - trader_level)+" (100 = Every time), or enter 'h' for more information or 'c' to cancel changes:\n\n > ")

            if chance == "c":
                print("\n#####################################\n\nChanges to the config cancelled!\n\n#####################################")
                return False
            elif chance == "h":
                print("\nTrader Chance Explanation: *****\n\nEach trader chance is part of the same RNG roll.\nSo, setting trader level 4's chance to 5%, level 3 to 15%, and level 2 to 45%:\n\t 0-5% = Trader level 4\n\t 5.1%-15%: Trader level 3\n\t 16.1%-45%: Trader level 2\n\t 46.1%-100.0%: Trader level 1")
                chance = ""
            else:
                configset.tr_lvl_chances[trader_level] = float(chance)/100.0
                print("\nSet the chance for trader level "+str(4 - trader_level)+" to "+str(configset.tr_lvl_chances[trader_level]*100)+"%!")
                configset.saveconfig()
                break_flag = True

    elif mod_input == "2": # labs option
        mod_input = input("\nThank you, please enter 'y' or 'n' for allowing The Lab to be the starting map, or 'c' to cancel changes:\n\n > ")

        while not (mod_input == "y" or mod_input == "n" or mod_input == "c"):
            mod_input = input("\nThat is an invalid response. Please enter 'y' or 'n' for allowing The Lab to be the starting map, or 'c' to cancel changes:\n\n > ")
        
        if mod_input == "y":
            configset.labs_only_dest = False
        elif mod_input == "n":
            configset.labs_only_dest = True
        else:
            print("\n#####################################\n\nChanges to the config cancelled!\n\n#####################################")
            return False

        configset.saveconfig()

    elif mod_input == "3": # fence option
        mod_input = input("\nThank you, please enter 'y' or 'n' for allowing Fence to be a trader, or 'c' to cancel changes:\n\n > ")

        while not (mod_input == "y" or mod_input == "n" or mod_input == "c"):
            mod_input = input("\nThat is an invalid response. Please enter 'y' or 'n' for allowing Fence to be a trader, or 'c' to cancel changes:\n\n > ")
        
        if mod_input == "y":
            configset.fence_allowed = True
        elif mod_input == "n":
            configset.fence_allowed = False
        else:
            print("\n#####################################\n\nChanges to the config cancelled!\n\n#####################################")
            return False

        configset.saveconfig()

def main():
    print("#####################################\n\nWelcome to the Escape From Tarkov Campaign Generation tool!\n")
    break_flag = False 

    while break_flag == False:
        u_response = input("\nSelect the action you'd like to take:\n1. Edit Config\n2. Generate Campaign\n3. Exit the Program\n\n > ")

        print("\n#####################################")
        if u_response == "1":
            edit_config()
        elif u_response == "2":
            gen_campaign()
        elif u_response == "3": 
            print("\n\nThank you for using the Escape From Tarkov campaign generator.")
            break_flag = True
        
if __name__ == "__main__":
    main()