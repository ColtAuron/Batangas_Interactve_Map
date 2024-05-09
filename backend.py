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
    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type="Animal"):
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

    def __init__(self, Name, sciName, desc, xPos, yPos, img, city, type="Plant"):
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

    def __init__(self, Name, link, desc, xPos, yPos, img, city, type="Tourist Destination"):
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
        self.con = sqlite3.connect(db_path)
        self.c = self.con.cursor()

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
        self.left_frame = CTkFrame(self, width=frame_width, height=frame_height, fg_color="#BEEF9E")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.create_button()

        logo_path = os.path.join(BASE_DIR, "icons", "logo.png")
        logo_image = logo_path
        logo_image = CTkImage(Image.open(logo_image), size=(250, 250))
        logo_label = CTkLabel(self.left_frame, image=logo_image, bg_color="#BEEF9E", text="")
        logo_label.place(x=0, y=0)
        logo_label.image = logo_image

        self.dropdown = customtkinter.CTkOptionMenu(self.left_frame,
                                                    values=["Category", "Animal", "Plant", "Tourist Spot"],
                                                    command=self.dropdown_callback, fg_color="#828C51",
                                                    dropdown_fg_color="#A6C36F", dropdown_hover_color="#6B7342", font=
                                                    ('Arial', 14, 'bold'), dropdown_font=('Arial', 14, 'bold'),
                                                    button_color="#A6C36F", button_hover_color="#828C51",
                                                    text_color="#000000", dropdown_text_color="#000000")
        self.colt = False
        self.Name = customtkinter.CTkLabel(self.left_frame, text="Name:", text_color="Black")
        self.Namebox = customtkinter.CTkEntry(self.left_frame, width=140, height=10, corner_radius=1)
        self.Sci = customtkinter.CTkLabel(self.left_frame, text="Scientific Name:", text_color="Black")
        self.Scibox = customtkinter.CTkEntry(self.left_frame, width=140, height=10, corner_radius=1)
        self.Desc = customtkinter.CTkLabel(self.left_frame, text="Description:", text_color="Black")
        self.DescBox = customtkinter.CTkEntry(self.left_frame, width=140, height=10, corner_radius=1)
        self.Link = customtkinter.CTkLabel(self.left_frame, text="Link:", text_color="Black")
        self.LinkBox = customtkinter.CTkEntry(self.left_frame, width=140, height=10, corner_radius=1)
        self.suggest = customtkinter.CTkButton(self.left_frame, width=140, height=10, text="Submit", fg_color="#A6C36F"
                                               ,text_color="#000000", hover_color="#828C51",font=('Arial', 14, 'bold'), command=self.suggest_button)

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

        self.sgXpoint = None
        self.sgYpoint = None
        self.sgCurMar = None
        self.choice = None

    def create_button(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        animal_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "animal.png")))
        plant_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "plant.png")))
        tourist_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "tourist.png")))
        cities_icon = customtkinter.CTkImage(Image.open(os.path.join(file_path, "icons", "city.png")))

        button_names = ["Animals", "Plants", "Tourist Spots", "Cities",
                        "Suggestions"]
        icons = [animal_icon, plant_icon, tourist_icon, cities_icon, None]

        buttons = []
        button_states = {name: False for name in button_names}

        for i, (name, icon) in enumerate(zip(button_names, icons)):
            def click_callback(name):   #color activation/deactivation if click
                def on_click():
                    self.on_click(name)
                    if name == "Suggestions":
                        button_states[name] = not button_states[name]
                        if button_states[name]:
                            buttons[button_names.index(name)].configure(fg_color="#A6C36F")
                        else:
                            buttons[button_names.index(name)].configure(fg_color="#828C51")
                    else:
                        button_states[name] = not button_states[name]
                        if button_states[name]:
                            buttons[button_names.index(name)].configure(fg_color="#A6C36F")
                        else:
                            buttons[button_names.index(name)].configure(fg_color="#828C51")

                return on_click

            if icon is not None:
                button = CTkButton(self.left_frame, image=icon, compound="left", text=name,
                                   command=click_callback(name), text_color="#000000",
                                   font=('Arial', 14, 'bold'), fg_color="#828C51", hover_color="#A6C36F")
            else:
                button = CTkButton(self.left_frame, text=name, command=click_callback(name),
                                   text_color="#000000", font=('Arial', 14, 'bold'),
                                   fg_color="#828C51", hover_color="#A6C36F")

            button.grid(row=i, column=0, padx=(50, 50), pady=(250, 5) if name == "Animals" else 5, sticky="ew")
            buttons.append(button)

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
                self.animalMarkers.append(
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.animal_active,
                                               icon=self.animalimg, icon_anchor="s", text_color="#d1ae69"))
                self.animalInfo.append([item.sciName, item.desc, item.img, item.city])
        else:
            for animal in self.animalMarkers:
                self.map_widget.delete(animal)
            self.animalMarkers.clear()
            Animals.all.clear()
            self.plantInfo.clear()

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
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.plant_active,
                                               icon_anchor="s", icon=self.plantimg, text_color="#7cd169"))
                self.plantInfo.append([item.sciName, item.desc, item.img, item.city])
        else:
            for plant in self.plantMarkers:
                self.map_widget.delete(plant)
            self.plantMarkers.clear()
            Plants.all.clear()
            self.plantInfo.clear()

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
                    self.map_widget.set_marker(item.xPos, item.yPos, item.Name, command=self.tourist_active,
                                               icon_anchor="s", icon=self.T_img, text_color="#d16a6a"))
                self.touristInfo.append([item.link, item.desc, item.img, item.city])
        else:
            for tourist in self.touristMarkers:
                self.map_widget.delete(tourist)
            self.touristMarkers.clear()
            TouristDes.all.clear()
            self.touristInfo.clear()

    def load_city_markers(self):
        if self.cityMarkers == []:
            #                        0        1        2         3        4          5     6      7     8      9
            self.c.execute("Select Name, District, Population, Width, Description, Image, Link, xPos, yPos, Disabled From Cities_Loc, City WHERE Cities_Loc.CityID = City.CityID")
            frSql = self.c.fetchall()
            for items in frSql:
                if(items[9] == 0):
                    self.cityMarkers.append(self.map_widget.set_marker(items[7],items[8],items[0], command = self.cities_active, icon_anchor = "s", icon = self.M_img, text_color = "#6987d1"))
                    self.cityInfo.append([items[1],items[2],items[3],items[4],items[5],items[6]])
        else:
            for item in self.cityMarkers:
                self.map_widget.delete(item)
            self.cityMarkers.clear()
            self.cityInfo.clear()
        pass

    def load_suggestions(self):
        if (self.colt == False):
            self.dropdown.place(x=50, y=450)
            self.bind('<space>', self.toggle_coords)
            self.colt = True
            if self.sgXpoint and self.sgYpoint:
                self.drawSGMarker()
        else:
            if self.sgCurMar:
                self.map_widget.delete(self.sgCurMar)
                self.sgCurMar = None
            self.unbind('<space>')  
            self.dropdown.place_forget()
            self.colt = False
    
    def toggle_coords(self, event=None):
        if self.map_widget.canvas.cget('cursor') == 'arrow':
            self.map_widget.canvas.config(cursor="tcross")
            self.map_widget.canvas.unbind("<B1-Motion>")
            self.map_widget.canvas.unbind("<Button-1>")
            self.map_widget.canvas.bind("<Button-1>", self.draw_coords)
            self.bind("<Control-z>", self.undo_draw_coords)
        else:
            self.map_widget.canvas.config(cursor="arrow")
            self.map_widget.canvas.unbind("<Button-1>")
            self.unbind("<Control-z>")
            self.map_widget.canvas.bind("<B1-Motion>", self.map_widget.mouse_move)
            self.map_widget.canvas.bind("<Button-1>", self.map_widget.mouse_click)
    
    def draw_coords(self, event=(0,0)):
        raw_mouse = self.map_widget.convert_canvas_coords_to_decimal_coords(canvas_x=event.x,canvas_y=event.y)
        mouse_pos = tuple((round(raw_mouse[0], 7),round(raw_mouse[1], 7)))
        self.sgXpoint = mouse_pos[0]
        self.sgYpoint = mouse_pos[1]
        self.drawSGMarker()
        pass

    def drawSGMarker(self):
        if self.sgCurMar:
            self.map_widget.delete(self.sgCurMar)
            self.sgCurMar = self.map_widget.set_marker(self.sgXpoint, self.sgYpoint)
        else:
            self.sgCurMar = self.map_widget.set_marker(self.sgXpoint, self.sgYpoint)

    def undo_draw_coords(self, event = None): #needed kasi tatawagin din sa submit
        self.sgXpoint = None
        self.sgYpoint = None
        if self.sgCurMar:
            self.map_widget.delete(self.sgCurMar)
            self.sgCurMar = None
        pass

    def dropdown_callback(self, choice):
        self.choice = choice
        self.Namebox.delete(0, len(self.Namebox.get()))
        self.Scibox.delete(0, len(self.Scibox.get()))
        self.DescBox.delete(0, len(self.DescBox.get()))
        self.LinkBox.delete(0, len(self.LinkBox.get()))
        if (choice == "Category"):
            self.forget_everything()
        elif (choice == "Animal" or choice == "Plant"):
            self.forget_everything()
            self.Name.place(x=50, y=480)
            self.Namebox.place(x=50, y=500)
            self.Sci.place(x=50, y=530)
            self.Scibox.place(x=50, y=550)
            self.Desc.place(x=50, y=580)
            self.DescBox.place(x=50, y=600)
            self.Link.place(x=50, y=630)
            self.LinkBox.place(x=50, y=650)
            self.suggest.place(x=50, y=700)
        elif (choice == "Tourist Spot"):
            self.forget_everything()
            self.Name.place(x=50, y=480)
            self.Namebox.place(x=50, y=500)
            self.Desc.place(x=50, y=530)
            self.DescBox.place(x=50, y=550)
            self.Link.place(x=50, y=580)
            self.LinkBox.place(x=50, y=600)
            self.suggest.place(x=50, y=650)

    def suggest_button(self):
        if self.Namebox.get() and self.DescBox.get() and self.LinkBox.get() and (self.choice == 'Tourist Spot' or (self.Scibox.get())):
            name = self.Namebox.get()
            sci = self.Scibox.get()
            desc = self.DescBox.get()
            link = self.LinkBox.get()
            if self.sgCurMar:
                x = self.sgXpoint
                y = self.sgYpoint
                print(name,sci,desc,link,x,y)
                self.Namebox.delete(0, len(self.Namebox.get()))
                self.Scibox.delete(0, len(self.Scibox.get()))
                self.DescBox.delete(0, len(self.DescBox.get()))
                self.LinkBox.delete(0, len(self.LinkBox.get()))
                self.undo_draw_coords()
                if sci == "":
                    sci = "NULL"
                to_database = tuple((self.choice, name, sci, desc, link, x, y))
                self.c.execute("INSERT INTO SUGGEST (Category, Name, SciName, Description, Link, xPos, yPos) VALUES (?,?,?,?,?,?,?)", to_database)
                self.con.commit()
                print("Submitted Successfully!")
            else:
                print("Put out a marker")
        else:
            print(self.current_category)
            print("Fill out")
            

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
        print(sciName, desc, img, city) #otivs dito ka magfunc ng popout
        
        animal_window = customtkinter.CTkToplevel(self)
        animal_window.title("Animals")
        animal_window.geometry("800x600+0x0")
        animal_window.resizable(False, False)
        animal_window.attributes("-topmost", True)

    def plant_active(self, marker):
        sciName = self.plantInfo[self.plantMarkers.index(marker)][0]
        desc = self.plantInfo[self.plantMarkers.index(marker)][1]
        img = self.plantInfo[self.plantMarkers.index(marker)][2]
        city = self.plantInfo[self.plantMarkers.index(marker)][3]
        print(sciName, desc, img, city) #otivs dito ka magfunc ng popout
        
        plant_window = customtkinter.CTkToplevel(self)
        plant_window.title("Plants")
        plant_window.geometry("800x600+0x0")
        plant_window.resizable(False, False)
        plant_window.attributes("-topmost", True)

    def tourist_active(self, marker):
        link = self.touristInfo[self.touristMarkers.index(marker)][0]
        desc = self.touristInfo[self.touristMarkers.index(marker)][1]
        img = self.touristInfo[self.touristMarkers.index(marker)][2]
        city = self.touristInfo[self.touristMarkers.index(marker)][3]
        print(link, desc, img, city) #otivs dito ka magfunc ng popout
        
        tourist_window = customtkinter.CTkToplevel(self)
        tourist_window.title("Tourist")
        tourist_window.geometry("800x600+0x0")
        tourist_window.resizable(False, False)
        tourist_window.attributes("-topmost", True)

    def cities_active(self, marker):
        district = self.cityInfo[self.cityMarkers.index(marker)][0]
        population = self.cityInfo[self.cityMarkers.index(marker)][1]
        width = self.cityInfo[self.cityMarkers.index(marker)][2]
        description = self.cityInfo[self.cityMarkers.index(marker)][3]
        image = self.cityInfo[self.cityMarkers.index(marker)][4]
        link = self.cityInfo[self.cityMarkers.index(marker)][5]
        print(district, population, width, description, image, link) #otivs dito ka magfunc ng popout
        
        city_window = customtkinter.CTkToplevel(self)
        city_window.title("Cities")
        city_window.geometry("800x600+0x0")
        city_window.resizable(False, False)
        city_window.attributes("-topmost", True)

    def start(self):
        self.mainloop()


# Remove this if Implement to Front
if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.start()
