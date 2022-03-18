# EFTCampaignGenerator
A standalone program intended for use with the game Escape From Tarkov, developed by Battlestate Games. Contains both a GUI and a console version of a randomized campaign generator. Includes seeding campaigns as well as customizing some aspects of the generated campaigns.

# REQUIREMENTS
The program is written in Python, so you must have Python installed to run this.
To run the console version (program_console.py), no additional libraries are needed.
To run the GUI version (program_ui.py), you must have Tkinter as well as Pillow installed. 

# COMPLETE FEATURES
- Randomized campaign generator, 2-6 maps long, with a specified start and finish.
- Randomized traders and trader levels at each location, with the intention that only that trader and the levels generated are available when entering that location
- Campaigns display a seed, and entering a seed with the same campaign size will reproduce another's campaign
- Customizable chance for higher trader levels, allowing the campaign to begin at The Lab, and allowing Fence to be selected as a random trader encounter.
- The GUI version and the console version have the same capabilities
