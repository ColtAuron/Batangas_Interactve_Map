import tkinter
from tkintermapview import *
import tkintermapview
import os
import sqlite3
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
class Animals:
    all = []
    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type = "Animal"):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        Animals.all.append(self)

class Plants:
    all = []
    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type = "Plant"):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        self.all.append(self)

class TouristDes:
    all = []
    def __init__(self, Name, link, desc, xPos, yPos, img, city, type = "Tourist Destination"):
        self.Name = Name
        self.link = link
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        self.all.append(self)

class Biomes:
    all=[]
    def __init__(self, Name, desc, xPos, yPos, img, city, type = 'Biome'):
        self.Name = Name
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.all.append(self)


class HoverMapView(TkinterMapView):
    def __init__(self, left_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_frame = left_frame

class App(customtkinter.CTk):
    app_name = "Batangas Interactive Map"
    width = 1280
    height = 800


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "bimData.db")
        con = sqlite3.connect(db_path)
        self.c = con.cursor()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "batangas.db")

        self.title(App.app_name)
        frame_width = 1280
        frame_height = App.height

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.CenterX = int((self.screen_width - App.width) / 2)
        self.CenterY = int((self.screen_height - App.height) / 2)
        self.geometry(f"{App.width}x{App.height}+{self.CenterX}+{self.CenterY}")
        self.minsize(App.width, App.height)

        window_logo_path = os.path.join(BASE_DIR, "icons", "window_logo.ico")
        self.iconbitmap(window_logo_path)

        self.current_category = None

        # left frame
        self.left_frame = CTkFrame(self, width=frame_width, height=frame_height,fg_color="#BEEF9E")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.create_button()

        logo_path = os.path.join(BASE_DIR, "icons", "logo.png")
        logo_image = logo_path
        logo_image = CTkImage(Image.open(logo_image), size=(250,250))
        logo_label = CTkLabel(self.left_frame, image=logo_image, bg_color="#BEEF9E", text="")
        logo_label.place(x=0,y=0)
        logo_label.image = logo_image

        # right frame
        self.right_frame = CTkFrame(self, width=frame_width, height=frame_height)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(self.right_frame, width=800, height=700,
                                                        database_path=database_path, corner_radius=0)
        self.map_widget.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
        # 13.8525866, 121.0435568
        self.map_widget.set_position(deg_x=13.7582328, deg_y=121.0726133)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_zoom(13)
        self.reload_markers()

        self.animalMarkers = []
        self.animalInfo = []
        self.plantMarkers = []
        self.plantInfo = []
        self.touristMarkers = []
        self.touristInfo = []
        self.biomeMarkers = []
        self.biomeInfo = []

    def create_button(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        animal_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "animal.png")))
        plant_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "plant.png")))
        tourist_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "tourist.png")))

        button_names = ["Animals", "Plants", "Tourist Spots",
                        "Suggestions"]
        icons = [animal_icon, plant_icon, tourist_icon, None]

        for i, (name, icon) in enumerate(zip(button_names, icons)):
            if icon is not None:
                button = CTkButton(self.left_frame, image=icon, compound="left", text=name,
                                   command=lambda n=name: self.on_click(n), text_color="#000000",
                                   font=('Arial', 14, 'bold'), fg_color="#A6C36F", hover_color="#828C51")
            else:
                button = CTkButton(self.left_frame, text=name, command=lambda n=name: self.on_click(n),
                                   text_color="#000000", font=('Arial', 14, 'bold'), fg_color="#A6C36F",
                                   hover_color="#828C51")

            button.grid(row=i, column=0, padx=(50, 50), pady=(250, 5) if name == "Animals" else 5, sticky="ew")

    def on_click(self, category):
        self.current_category = category
        self.reload_markers()

    def reload_markers(self):  
        if self.current_category == "Animals":
            self.load_animal_markers()
        elif self.current_category == "Plants":
            self.load_plant_markers()
        elif self.current_category == "Tourist Spots":
            self.load_tourist_markers()
        elif self.current_category == "Suggestions":
            self.load_biome_markers()

    def load_animal_markers(self):
        if self.animalMarkers == []:
            self.c.execute(
                "Select Animal.Name, sciName, desc, img, City.Name, xPos, yPos, Disabled From AnimalsLoc, Animal, City WHERE AnimalsLoc.AnimalID = Animal.AnimalID AND AnimalsLoc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[7] == 0):
                    Animals(items[0], items[1], items[2], items[5], items[6], items[3], items[4])
            for item in Animals.all:
                self.animalMarkers.append(self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.animal_active))
                self.animalInfo.append([item.sciName, item.desc, item.img, item.city])

            #
            # Add button activated func 
            #

        else:
            for animal in self.animalMarkers:
                self.map_widget.delete(animal)
            self.animalMarkers.clear()
            Animals.all.clear()
            self.plantInfo.clear()
            #
            # Revert to Normal pre-activated
            #

    def load_plant_markers(self):
        if self.plantMarkers == []:
            self.c.execute(
                "Select Plant.Name, sciName, desc, img, City.Name, xPos, yPos, Disabled From PlantsLoc, Plant, City WHERE PlantsLoc.PlantsID = Plant.PlantID AND PlantsLoc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[7] == 0):
                    Plants(items[0], items[1], items[2], items[5], items[6], items[3], items[4])
            for item in Plants.all:
                self.plantMarkers.append(
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.plant_active))
                self.plantInfo.append([item.sciName, item.desc, item.img, item.city])
            #
            # Add button activated func 
            #
        else:
            for plant in self.plantMarkers:
                self.map_widget.delete(plant)
            self.plantMarkers.clear()
            Plants.all.clear()
            self.plantInfo.clear()
            #
            # Revert to Normal pre-activated
            #

    def load_tourist_markers(self):
        if self.touristMarkers == []:
            self.c.execute(
                "Select Tourist.Name, link, desc, img, City.Name, xPos, yPos, Disabled From TouristLoc, Tourist, City WHERE TouristLoc.TouristID = Tourist.TouristID AND TouristLoc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[7] == 0):
                    TouristDes(items[0], items[1], items[2], items[5], items[6], items[3], items[4])
            for item in TouristDes.all:
                self.touristMarkers.append(
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.tourist_active))
                self.touristInfo.append([item.link, item.desc, item.img, item.city])
        else:
            for tourist in self.touristMarkers:
                self.map_widget.delete()
            self.touristMarkers.clear()
            TouristDes.all.clear()
            self.touristInfo.clear()

    def load_biome_markers(self):
        if self.biomeMarkers == []:
            self.c.execute(
                "Select Biome.Name, desc, img, City.Name, xPos, yPos, Disabled From BiomeLoc, Biome, City WHERE BiomeLoc.BiomeID = Biome.BiomeID AND BiomeLoc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[6] == 0):
                    Biomes(items[0], items[1], items[4], items[5], items[2], items[3])
            for item in Biomes.all:
                self.biomeMarkers.append(
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.biome_active))
                self.biomeInfo.append([item.desc, item.img, item.city])
        else:
            for biome in self.biomeMarkers:
                self.map_widget.delete(biome)
            self.biomeMarkers.clear()
            Biomes.all.clear()
            self.biomeInfo.clear()

    def animal_active(self, marker):
        sciName = self.animalInfo[self.animalMarkers.index(marker)][0]
        desc = self.animalInfo[self.animalMarkers.index(marker)][1]
        img = self.animalInfo[self.animalMarkers.index(marker)][2]
        city = self.animalInfo[self.animalMarkers.index(marker)][3]
        print(sciName, desc, img, city)

    def plant_active(self, marker):
        sciName = self.plantInfo[self.plantMarkers.index(marker)][0]
        desc = self.plantInfo[self.plantMarkers.index(marker)][1]
        img = self.plantInfo[self.plantMarkers.index(marker)][2]
        city = self.plantInfo[self.plantMarkers.index(marker)][3]
        print(sciName, desc, img, city)

    def tourist_active(self, marker):
        link = self.touristInfo[self.touristMarkers.index(marker)][0]
        desc = self.touristInfo[self.touristMarkers.index(marker)][1]
        img = self.touristInfo[self.touristMarkers.index(marker)][2]
        city = self.touristInfo[self.touristMarkers.index(marker)][3]
        print(link, desc, img, city)

    def biome_active(self, marker):
        desc = self.biomeInfo[self.biomeMarkers.index(marker)][0]
        img = self.biomeInfo[self.biomeMarkers.index(marker)][1]
        city = self.biomeInfo[self.biomeMarkers.index(marker)][2]
        print(desc, img, city)

    def start(self):
        self.mainloop()

#Remove this if Implement to Front
if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.start()