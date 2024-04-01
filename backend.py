#animals
#tourist destinations
#types of biomes
#plants
import tkinter
import tkintermapview

tk = tkinter.Tk()
tk.geometry(f"{800}x{600}")

map_widget = tkintermapview.TkinterMapView(tk, width=800, height= 600, corner_radius=0)
map_widget.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
map_widget.set_position(13.8525866, 121.0435568)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
map_widget.set_zoom(10)

tk.mainloop()

class Animals:
    def __init__(self, Name, sciName, desc, xPos, yPos, img):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img

class Plants:
    def __init__(self, Name, sciName, desc, xPos, yPos, img):
        self.Name = Name
        self.sciName = sciName
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img

class TouristDes:
    def __init__(self, Name, link, desc, xPos, yPos, img):
        self.Name = Name
        self.link = link
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img

class Biomes:
    def __init__(self, Name, type, desc, xPos, yPos, img):
        self.Name = Name
        self.type = type
        self.desc = desc
        self.xPos = xPos
        self.yPos = yPos
        self.img = img



