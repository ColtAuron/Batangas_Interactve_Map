import tkinter
import tkintermapview
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bimData.db")
con = sqlite3.connect(db_path)
c = con.cursor()

class Animals:
    all = []
    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type = "Animal", disabled=False):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        self.disabled = disabled
        Animals.all.append(self)

animal_table = []
c.execute("Select Animal.Name, sciName, desc, img, City.Name, xPos, yPos From AnimalsLoc, Animal, City WHERE AnimalsLoc.AnimalID = Animal.AnimalID AND AnimalsLoc.CityID = City.CityID")
frSql = c.fetchall()
for items in frSql:
    Animals(items[0], items[1], items[2], items[5], items[6], items[3], items[4])

class Plants:
    all = []
    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type = "Plant", disabled = False):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        self.disabled = disabled
        self.all.append(self)

plant_table = []
c.execute("Select Plant.Name, sciName, desc, img, City.Name, xPos, yPos From PlantsLoc, Plant, City WHERE PlantsLoc.PlantsID = Plant.PlantID AND PlantsLoc.CityID = City.CityID")
frSql = c.fetchall()
for items in frSql:
    Plants(items[0], items[1], items[2], items[5], items[6], items[3], items[4])


class TouristDes:
    all = []
    def __init__(self, Name, link, desc, xPos, yPos, img, city, type = "Tourist Destination", disabled = False):
        self.Name = Name
        self.link = link
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.type = type
        self.disabled = disabled
        self.all.append(self)

Tour_table = []
c.execute("Select Tourist.Name, link, desc, img, City.Name, xPos, yPos From TouristLoc, Tourist, City WHERE TouristLoc.TouristID = Tourist.TouristID AND TouristLoc.CityID = City.CityID")
frSql = c.fetchall()
for item in frSql:
    TouristDes(item[0], item[1], item[2], item[5], item[6], item[3], item[4])

class Biomes:
    all=[]
    def __init__(self, Name, desc, xPos, yPos, img, city, type = 'Biome', disabled = False):
        self.Name = Name
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img
        self.city = city
        self.disabled = disabled
        self.all.append(self)

Biome_table = []
c.execute("Select Biome.Name, desc, img, City.Name, xPos, yPos From BiomeLoc, Biome, City WHERE BiomeLoc.BiomeID = Biome.BiomeID AND BiomeLoc.CityID = City.CityID")
frSql = c.fetchall()
for item in frSql:
    Biomes(item[0], item[1], item[4], item[5], item[2], item[3])


class App():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tk = tkinter.Tk()
        self.tk.geometry(f"{800}x{600}")  

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "batangas.db")

        self.map_widget = tkintermapview.TkinterMapView(self.tk, width=800, height= 600, database_path=database_path, corner_radius=0)
        self.map_widget.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
        #13.8525866, 121.0435568
        self.map_widget.set_position(deg_x=13.7582328,deg_y=121.0726133)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_zoom(13)

        self.animalMarkers = []
        self.animalInfo = [] 
        self.plantMarkers = []
        self.plantInfo = []
        self.touristMarkers = []
        self.touristInfo = []
        self.biomeMarkers = []
        self.biomeInfo = []
        
        for item in Animals.all:
            self.animalMarkers.append(self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.animal_active),)
            self.animalInfo.append([item.sciName, item.desc, item.img, item.city])
        for item in Plants.all:
            self.plantMarkers.append(self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.plant_active),)
            self.plantInfo.append([item.sciName, item.desc, item.img, item.city])
        for item in TouristDes.all:
            self.plantMarkers.append(self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.tourist_active),)
            self.plantInfo.append([item.link, item.desc, item.img, item.city])
        for item in Biomes.all:
            self.biomeMarkers.append(self.map_widget.set_marker(item.xPos,item.yPos, item.Name, command=self.biome_active),)
            self.biomeInfo.append([item.desc, item.img, item.city])

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
        link = self.plantInfo[self.plantMarkers.index(marker)][0]
        desc = self.plantInfo[self.plantMarkers.index(marker)][1]
        img = self.plantInfo[self.plantMarkers.index(marker)][2]
        city = self.plantInfo[self.plantMarkers.index(marker)][3]
        print(link, desc, img, city)

    def biome_active(self, marker):
        desc = self.biomeInfo[self.biomeMarkers.index(marker)][0]
        img = self.biomeInfo[self.biomeMarkers.index(marker)][1]
        city = self.biomeInfo[self.biomeMarkers.index(marker)][2]
        print(desc, img, city)

    def start(self):
        self.tk.mainloop()
    
#Remove this if Implement to Front
if __name__ == "__main__":
    app = App()
    app.start()

