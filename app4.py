
import tkinter.messagebox
import customtkinter
import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import Canvas
 

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Instalocker")
        self.geometry(f"{1080}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0), weight=0)
        self.grid_rowconfigure(( 1), weight=1)
 

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,0))
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search")
        #search bar
        self.entry.grid(row=0, column=1, columnspan=2, rowspan= 1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.start_btn = customtkinter.CTkButton(self.sidebar_frame,text= "Start" )
        self.start_btn.grid(row=6, column=0, padx=20, pady=(10,20))
        self.path_btn = customtkinter.CTkButton(self.sidebar_frame,text= "Path" )
        self.path_btn.grid(row=2, column=0, padx=20, pady=(10,20))
        
        
        #role call
        self.text_label = customtkinter.CTkLabel(self.sidebar_frame, text="Role:", anchor="w")
        self.text_label.grid(row=3, column=0, padx=20, pady=(10, 20))
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame,  width=30, height=20)
        self.textbox.grid(row=4, column=0, rowspan= 1, padx=20, pady=(10,10), sticky="nsew")
        self.textbox.grid_rowconfigure(5, weight=10)
        #switch
        instalock = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Instalock")
        instalock.grid(row=5, column=0, padx=10, pady=(20, 20))
        
        
        
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=1,  rowspan=4, padx=(20, 20), pady=(0, 60), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=0)

        
        
        
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
