import tkinter as tk
from PIL import ImageTk, Image
import requests
import json
import urllib.request
import io



url = "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json"

response = urllib.request.urlopen(url)
data = json.loads(response.read())



class ChampionBrowser(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("League of Legends Champion Browser")
        
        # Set up the search bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_champions)
        self.search_entry = tk.Entry(self.master, textvariable=self.search_var)
        self.search_entry.pack()
        
        # Set up the canvas for the champion images
        self.canvas = tk.Canvas(self.master, width=300, height=500)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self.scroll_canvas)
        
        # Set up the frame to hold the champion images
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Load the champion images
        self.champions = []

        for champion in data["data"].values():
            champ = champion["id"]

            img_url = "http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/%s.png" % champ
            img_data = urllib.request.urlopen(img_url).read()
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((64, 64), Image.ANTIALIAS)
            self.champions.append(ImageTk.PhotoImage(img))

            print("id:", champion["id"], "key:", champion["key"])
 
        # Display all the champion images
        self.update_champions()
    
    def update_champions(self, *args):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Get the search string
        search_str = self.search_var.get().lower()
        
        # Display the matching champions
        row_num = 0
        col_num = 0
        for i, champ in enumerate(self.champions):
            if search_str in str(i+1) or search_str in champ.name.lower():
                champ_label = tk.Label(self.frame, image=champ)
                champ_label.grid(row=row_num, column=col_num, padx=5, pady=5)
                col_num += 1
                if col_num == 5:
                    col_num = 0
                    row_num += 1
    
    def resize_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def scroll_canvas(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root = tk.Tk()
app = ChampionBrowser(master=root)
app.mainloop()
