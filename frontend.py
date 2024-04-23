import customtkinter
from customtkinter import *


class App(customtkinter.CTk):
    app_name = "Batangas Interactive Map"
    width = 800
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.app_name)
        self.width = int(self.winfo_screenwidth()/2.5)
        self.height = int(self.winfo_screenheight()/2)
        self.geometry(f"{self.width}x{self.height})")
        self.minsize(500,500)
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.CenterX = int((self.screen_width-App.width)/2)
        self.CenterY = int((self.screen_height-App.height)/2)
        self.geometry(f"{App.width}x{App.height}+{self.CenterX}+{self.CenterY}")
        self.minsize(App.width, App.height)

if __name__ == "__main__":
    app = App()
    app.mainloop()