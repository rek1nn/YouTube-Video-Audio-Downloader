import tkinter as tk
from typing import Optional, Tuple, Union
import customtkinter
from pytube import YouTube 

# Theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue") # blue, dark-blue, green

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Configurate window
        self.title("YouLoader")
        self.geometry("1100x580")

        # Create an entry for URL
        url_var = tk.StringVar()
        url_entry_btn = customtkinter.CTkEntry(self,
                                           placeholder_text="Enter URL here...",
                                           textvariable=url_var,
                                           width=350,
                                           height=25)
        url_entry_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Simple button
        btn = customtkinter.CTkButton(self, text="Download", command=self.close_btn)
        btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    def close_btn(self):
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()