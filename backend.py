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
        db_path = os.path.join(BASE_DIR, "Batangas_IM.db")
        con = sqlite3.connect(db_path)
        self.c = con.cursor()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "batangas.db")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.animalimg = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "icons", "animalmarker.png")).resize((50, 70)))
        self.plantimg = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "icons", "plantmarker.png")).resize((50, 70)))
        self.T_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "icons", "touristmarker.png")).resize((50, 70)))
        self.M_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "icons", "marker.png")).resize((70, 70)))

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

        self.dropdown = customtkinter.CTkOptionMenu(self.left_frame, values=["Please Select One", "Animal", "Plant", "Tourist Spot"], command=self.dropdown_callback)
        self.colt = False
        self.Name = customtkinter.CTkLabel(self.left_frame, text="Name:", text_color="Black")
        self.Namebox = customtkinter.CTkTextbox(self.left_frame, width = 140, height = 10, corner_radius= 1)
        self.Sci = customtkinter.CTkLabel(self.left_frame, text="Scientific Name:", text_color="Black")
        self.Scibox = customtkinter.CTkTextbox(self.left_frame, width = 140, height = 10, corner_radius= 1)
        self.Desc = customtkinter.CTkLabel(self.left_frame, text="Description:", text_color="Black")
        self.DescBox = customtkinter.CTkTextbox(self.left_frame, width = 140, height = 10, corner_radius= 1)
        self.Link = customtkinter.CTkLabel(self.left_frame, text="Link:", text_color="Black")
        self.LinkBox = customtkinter.CTkTextbox(self.left_frame, width = 140, height = 10, corner_radius= 1)
        self.suggest = customtkinter.CTkButton(self.left_frame, width = 140, height = 10, text = "Submit")


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
        self.cityMarkers = []
        self.cityInfo = []

    def create_button(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        animal_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "animal.png")))
        plant_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "plant.png")))
        tourist_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "tourist.png")))

        button_names = ["Animals", "Plants", "Tourist Spots", "Cities",
                        "Suggestions"]
        icons = [animal_icon, plant_icon, tourist_icon, None, None]

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
        elif self.current_category == "Cities":
            self.load_city_markers()
        elif self.current_category == "Suggestions":
            self.load_suggestions()

    def load_animal_markers(self):
        if self.animalMarkers == []:
            self.c.execute(
                "Select Animal.Name, sciName, desc, img, City.Name, xPos, yPos, Disabled From AnimalsLoc, Animal, City WHERE AnimalsLoc.AnimalID = Animal.AnimalID AND AnimalsLoc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[7] == 0):
                    Animals(items[0], items[1], items[2], items[5], items[6], items[3], items[4])
            for item in Animals.all:
                self.animalMarkers.append(self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.animal_active, icon = self.animalimg, icon_anchor = "s",text_color = "#d1ae69"))
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
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.plant_active, icon_anchor = "s", icon = self.plantimg, text_color = "#7cd169"))
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
                "Select Tourist.Name, Tourist.Link, Tourist.Description, Tourist.Image, City.Name, xPos, yPos, Disabled From Tourist_Loc, Tourist, City WHERE Tourist_Loc.TouristID = Tourist.TouristID AND Tourist_Loc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if (items[7] == 0):
                    TouristDes(items[0], items[1], items[2], items[5], items[6], items[3], items[4])
            for item in TouristDes.all:
                self.touristMarkers.append(
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.tourist_active, icon_anchor = "s", icon = self.T_img, text_color = "#d16a6a"))
                self.touristInfo.append([item.link, item.desc, item.img, item.city])
            #
            # Add button activated func 
            #
        else:
            for tourist in self.touristMarkers:
                self.map_widget.delete(tourist)
            self.touristMarkers.clear()
            TouristDes.all.clear()
            self.touristInfo.clear()
            #
            # Revert to Normal pre-activated
            #

    def load_city_markers(self):
        if self.cityMarkers == []:
            #                        0        1        2         3        4          5     6      7     8      9
            self.c.execute("Select Name, District, Population, Width, Description, Image, Link, xPos, yPos, Disabled From Cities_Loc, City WHERE Cities_Loc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if(items[9] == 0):
                    self.cityMarkers.append(self.map_widget.set_marker(items[7],items[8],items[0], command = self.cities_active, icon_anchor = "s", icon = self.M_img, text_color = "#6987d1"))
                    self.cityInfo.append([items[1],items[2],items[3],items[4],items[5],items[6]])
            #
            # Add button activated func 
            #
        else:
            for item in self.cityMarkers:
                self.map_widget.delete(item)
            self.cityMarkers.clear()
            self.cityInfo.clear()
            #
            # Revert to Normal pre-activated
            #
        pass

    def load_suggestions(self):
        if (self.colt == False):
            self.dropdown.place(x=50, y=450)
            self.colt = True
        else:
            self.dropdown.place_forget()
            self.colt = False
    
    def dropdown_callback(self, choice):
        if(choice == "Please Select One"):
            self.forget_everything()
        elif(choice == "Animal" or choice == "Plant"):
            self.forget_everything()
            self.Name.place(x=50,y=480)
            self.Namebox.place(x=50, y=500)
            self.Sci.place(x=50,y=530)
            self.Scibox.place(x=50,y=550)
            self.Desc.place(x=50,y=580)
            self.DescBox.place(x=50,y=600)
            self.Link.place(x=50,y=630)
            self.LinkBox.place(x=50,y=650)
            self.suggest.place(x=50,y=700)
        elif(choice == "Tourist Spot"):
            self.forget_everything()
            self.Name.place(x=50,y=480)
            self.Namebox.place(x=50, y=500)
            self.Desc.place(x=50,y=530)
            self.DescBox.place(x=50,y=550)
            self.Link.place(x=50,y=580)
            self.LinkBox.place(x=50,y=600)
            self.suggest.place(x=50,y=650)

        
    def forget_everything(self):
        self.Name.place_forget()
        self.Namebox.place_forget()
        self.Sci.place_forget()
        self.Scibox.place_forget()
        self.Desc.place_forget()
        self.DescBox.place_forget()
        self.Link.place_forget()
        self.LinkBox.place_forget()
        self.suggest.place_forget()


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

    def cities_active(self, marker):
        pass

    def start(self):
        self.mainloop()

#Remove this if Implement to Front
if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.start()