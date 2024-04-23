import customtkinter
from customtkinter import *

class App(customtkinter.CTk):
    app_name = "Batangas Interactive Map"
    width = 800
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.app_name)

        # Define the width and height of the frames
        frame_width = App.width // 2
        frame_height = App.height

        # left frame
        self.left_frame = CTkFrame(self, width=frame_width, height=frame_height)
        self.left_frame.pack(side="left", fill="both", expand=True)

        button_names = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5"]

        for i, name in enumerate(button_names):
            button = CTkButton(self.left_frame, text=name)
            button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")

        # right frame
        self.right_frame = CTkFrame(self, width=frame_width, height=frame_height)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.CenterX = int((self.screen_width - App.width) / 2)
        self.CenterY = int((self.screen_height - App.height) / 2)
        self.geometry(f"{App.width}x{App.height}+{self.CenterX}+{self.CenterY}")
        self.minsize(App.width, App.height)

if __name__ == "__main__":
    app = App()
    app.mainloop()
