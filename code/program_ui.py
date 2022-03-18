# 
# Tarkov Campaign Generator - GUI
# 
# Author: MINDS3T/Fire8TheBlade
# Concept: MINDS3T/Fire8TheBlade and Kharjaro
# 

import config
import campaign_data
import random
import tkinter 

from tkinter import *
from PIL import Image, ImageTk

# Load and store the config data
window_config = config.ConfigSet()

# Visual offsets for each location, centered on (250,250) with the map size being 500x500
map_offsets = {
   "Factory": [-50,2],
   "Reserve": [-160,55],
   "Woods": [-97,-70],
   "Customs": [45,-57],
   "Interchange": [80,-95],
   "Shoreline": [-105,190],
   "The Lab": [-73,-173],
   "The Lab Intermediate": [0,-80],
   "Lighthouse": [-175,130],
   "Town": [-220,-37]
}

# Visual offset for the start and goal image labels
start_goal_off = [40,30]

class CampaignWindow:
   def __init__(self, win):
      self.window = win
      self.title_label = Label(win, text='Campaign Settings', fg='black',font=("Arial", 18))
      self.title_label.place(x=10, y=10)

      self.seed_label = Label(win, text='Seed')
      self.seed_label.place(x=70, y=55)
      self.seed_ent = Entry()
      self.seed_ent.place(x=25, y=75)
      self.random_seed_but = Button(win, text='Random Seed', command=self.random_seed)
      self.random_seed_but.place(x=45, y=100)

      self.map_label = Label(win, text='Map Count')
      self.map_label.place(x=45, y=135)
      self.map_count = IntVar(value=4)
      self.trader_2_chance = tkinter.Scale(
         win,
         from_=2,
         to=6,
         orient='horizontal',  # horizontal
         variable=self.map_count
      )
      self.trader_2_chance.place(x=25,y=155)
      self.trader_2_chance.set(4)

      self.tr_4_label = Label(win, text='Trader Lvl 4 Chance')
      self.tr_4_label.place(x=25, y=260)
      self.trader_4_chance = tkinter.Scale(
         win,
         from_=0,
         to=100, length=150,
         orient='horizontal',  # horizontal
         variable=window_config.tr_lvl_chances[0], command=self.save_config_slider
      )
      self.trader_4_chance.place(x=25,y=275)
      self.trader_4_chance.set(window_config.tr_lvl_chances[0]*100)
      self.tr_3_label = Label(win, text='Trader Lvl 3 Chance (If Not 4)')
      self.tr_3_label.place(x=25, y=335)
      self.trader_3_chance = tkinter.Scale(
         win,
         from_=0,
         to=100, length=150,
         orient='horizontal',  # horizontal
         variable=window_config.tr_lvl_chances[1], command=self.save_config_slider
      )
      self.trader_3_chance.place(x=25,y=350)
      self.trader_3_chance.set(window_config.tr_lvl_chances[1]*100)
      self.tr_2_label = Label(win, text='Trader Lvl 2 Chance (If Not 3)')
      self.tr_2_label.place(x=25, y=410)
      self.trader_2_chance = tkinter.Scale(
         win,
         from_=0,
         to=100,  length=150,
         orient='horizontal',  # horizontal
         variable=window_config.tr_lvl_chances[2], command=self.save_config_slider
      )

      self.trader_2_chance.place(x=25,y=425)
      self.trader_2_chance.set(window_config.tr_lvl_chances[2]*100)

      self.labs_only_var = BooleanVar(value=window_config.labs_only_dest)
      self.labs_only_end = Checkbutton(win, text="No Labs Start", variable=self.labs_only_var, command=self.save_config_check)
      self.labs_only_end.place(x=25, y=200)
      self.fence_allowed_var = BooleanVar(value=window_config.fence_allowed)
      self.fence_allowed_check = Checkbutton(win, text="Fence Allowed", variable=self.fence_allowed_var, command=self.save_config_check)
      self.fence_allowed_check.place(x=25, y=225)

      self.gen_campaign_but = Button(win, text='Generate Campaign', command=self.gen_campaign)
      self.gen_campaign_but.place(x=25, y=475)
      self.gen_campaign_but = Button(win, text='Generate Random Campaign', command=self.gen_random_campaign)
      self.gen_campaign_but.place(x=25, y=515)


      self.map_image = ImageTk.PhotoImage(Image.open("img/map.png").resize((500,500)))

      self.canvas = tkinter.Canvas(win,width=500,height=500)
      self.canvas.create_image(250,250, image=self.map_image)
      self.canvas.pack()
      self.canvas.place(relx=0.25,rely=0.1)

      self.trader_list_label = Label(self.window, text="Trader List",font=("Arial", 18))
      self.trader_list_label.place(x=750,y=10)
         
      self.missions_label = Label(self.window, text="Objectives",font=("Arial", 18))
      self.missions_label.place(x=750,y=225)

      
      # For updating traders in gen_campaign
      self.trader_labels = []

      self.gen_random_campaign()

   def gen_random_campaign(self):
      self.map_count.set(random.randint(2,6))
      self.random_seed()
      self.gen_campaign()

   def random_seed(self):
      self.seed_ent.delete(0, 'end') # Clear seed entry field
      self.seed_ent.insert(END,random.randint(100000000,999999999))

   def gen_campaign(self):
      if self.seed_ent.get() != '':
         # Re-create all the images relevant to each campaign so the old copies get removed from the canvas
         self.cur_campaign = campaign_data.Campaign(self.map_count.get(), int(self.seed_ent.get()), [self.trader_4_chance.get()/100.0,self.trader_3_chance.get()/100.0,self.trader_2_chance.get()/100.0], labs_final=not self.labs_only_var.get(), fence_allowed=self.fence_allowed_var.get())
         self.sel_image_1 = ImageTk.PhotoImage(Image.open("img/select_"+str(random.randint(0,1))+".png").rotate(random.randint(0,360)))
         self.sel_image_2 = ImageTk.PhotoImage(Image.open("img/select_"+str(random.randint(0,1))+".png").rotate(random.randint(0,360)))
         self.start_img = ImageTk.PhotoImage(Image.open("img/start.png"))
         self.start_point = ImageTk.PhotoImage(Image.open("img/point.png"))
         self.goal_img = ImageTk.PhotoImage(Image.open("img/goal.png"))
         self.town_point = ImageTk.PhotoImage(Image.open("img/point.png"))


         if hasattr(self,"primary_label"):
            self.primary_label.destroy()
            self.secondary_label.destroy()

         self.primary_label = Label(self.window, text="Primary Objective at "+self.cur_campaign.end_map+":\n  "+self.cur_campaign.mission_pri.replace("#","\n  "),justify=LEFT)
         self.primary_label.place(x=750,y=260)
         self.secondary_label = Label(self.window, text="Secondary Objective Throughout:\n  "+self.cur_campaign.mission_sec.replace("#","\n  "),justify=LEFT)
         self.secondary_label.place(x=750,y=440)

         print("Seed="+self.seed_ent.get()+", Size="+str(self.map_count.get())+", Path=",self.cur_campaign.full_path)

         # Label start and end maps
         self.canvas.create_image(250+map_offsets[self.cur_campaign.start_map][0],250+map_offsets[self.cur_campaign.start_map][1], image=self.sel_image_1)
         self.canvas.create_image(250+map_offsets[self.cur_campaign.start_map][0],250+map_offsets[self.cur_campaign.start_map][1], image=self.start_point)
         self.canvas.create_image(250+map_offsets[self.cur_campaign.start_map][0]+start_goal_off[0],250+map_offsets[self.cur_campaign.start_map][1]+start_goal_off[1], image=self.start_img)
         self.canvas.create_image(250+map_offsets[self.cur_campaign.end_map][0],250+map_offsets[self.cur_campaign.end_map][1], image=self.sel_image_2)
         self.canvas.create_image(250+map_offsets[self.cur_campaign.end_map][0]+start_goal_off[0],250+map_offsets[self.cur_campaign.end_map][1]+start_goal_off[1], image=self.goal_img)

         # Remove old lines, images and labels from previous generations
         if hasattr(self, 'canvas_lines') and len(self.canvas_lines) > 0:
            for line in self.canvas_lines:
               self.canvas.delete(line)

         if hasattr(self, 'point_images') and len(self.point_images) > 0:
            for line in self.point_images:
               self.canvas.delete(line)

         if hasattr(self, 'trader_labels') and len(self.trader_labels) > 0:
            for line in self.trader_labels:
               line.destroy()

         # Initialize the point for Town, since that needs to be added in special cases
         self.canvas.create_image(-100,-100, image=self.town_point)
         self.canvas_lines = []
         self.point_images = []
         self.trader_labels = []

         # Generate visual path between locations
         for i in range(0,len(self.cur_campaign.full_path)-1):
            map = self.cur_campaign.full_path[i]
            next_map = self.cur_campaign.full_path[i+1]

            if (map == "Lighthouse" and next_map == "Woods") or (map=="Woods" and next_map=="Lighthouse"):
               if i < len(self.cur_campaign.full_path)-1:
                  self.point_images.append(ImageTk.PhotoImage(Image.open("img/point.png")))
                  self.canvas.create_image(250+map_offsets[next_map][0],250+map_offsets[next_map][1], image=self.point_images[i])
                  self.canvas.create_image(250+map_offsets["Town"][0],250+map_offsets["Town"][1], image=self.town_point)
               
               self.canvas_lines.append(self.canvas.create_line(250+map_offsets[map][0],250+map_offsets[map][1],250+map_offsets["Town"][0],250+map_offsets["Town"][1], dash=(4,2),fill='red',width=2))
               self.canvas_lines.append(self.canvas.create_line(250+map_offsets["Town"][0],250+map_offsets["Town"][1],250+map_offsets[next_map][0],250+map_offsets[next_map][1], dash=(4,2),fill='red',width=2))
            else:
               if i < len(self.cur_campaign.full_path)-1:
                  self.point_images.append(ImageTk.PhotoImage(Image.open("img/point.png")))
                  self.canvas.create_image(250+map_offsets[next_map][0],250+map_offsets[next_map][1], image=self.point_images[i])

               if (map == "The Lab" and next_map == "Factory") or (map == "Factory" and next_map == "The Lab"):
                  self.canvas_lines.append(self.canvas.create_line(250+map_offsets["The Lab"][0],250+map_offsets["The Lab"][1],250+map_offsets["The Lab Intermediate"][0],250+map_offsets["The Lab Intermediate"][1], dash=(4,2),fill='red',width=2))
                  self.canvas_lines.append(self.canvas.create_line(250+map_offsets["The Lab Intermediate"][0],250+map_offsets["The Lab Intermediate"][1],250+map_offsets["Factory"][0],250+map_offsets["Factory"][1], dash=(4,2),fill='red',width=2))
               else:
                  self.canvas_lines.append(self.canvas.create_line(250+map_offsets[map][0],250+map_offsets[map][1],250+map_offsets[next_map][0],250+map_offsets[next_map][1], dash=(4,2),fill='red',width=2))

            # Generate labels for the current traders
            cur_trade = self.cur_campaign.trader_list[i]
            cur_trade_lvl = self.cur_campaign.trader_levels[i]

            if cur_trade_lvl > 1:
               self.trader_labels.append(Label(self.window, text=next_map + ": \n  " + cur_trade + " is here, level 1-"+str(cur_trade_lvl),justify=LEFT))
            else:
               self.trader_labels.append(Label(self.window, text=next_map + ": \n  " + cur_trade + " is here, level 1",justify=LEFT))

            self.trader_labels[len(self.trader_labels)-1].place(x=750,y=10+len(self.trader_labels)*35)

         self.canvas.pack()

   def save_config_slider(self,val):
      window_config.tr_lvl_chances = [self.trader_4_chance.get()/100.0,self.trader_3_chance.get()/100.0,self.trader_2_chance.get()/100.0]
      window_config.saveconfig()

   def save_config_check(self):
      window_config.labs_only_dest = not self.labs_only_var.get()
      window_config.fence_allowed = self.fence_allowed_var.get()
      window_config.saveconfig()

         

campaign_window = CampaignWindow(Tk())
campaign_window.window.resizable(False,False)
campaign_window.window.title('Escape From Tarkov Campaign Generator')
campaign_window.window.geometry("1000x550")
campaign_window.window.mainloop()
