import tkinter as tk
from tkinter import PhotoImage, Label
from PIL import Image
import customtkinter
from pytube import YouTube 
import os
import time

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
        self.url_var = tk.StringVar()
        self.url_entry = customtkinter.CTkEntry(self,
                                               textvariable=self.url_var,
                                               width=475,
                                               height=30)
        self.url_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
                
        # Create download button
        self.btn = customtkinter.CTkButton(
            self, text="Download", command=self.download_btn
        )
        self.btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Create checkbox for Video
        self.check_var_video = tk.StringVar(value="")

        self.checkbox_video = customtkinter.CTkCheckBox(self,
                                                   text="Video",
                                                   command=self.handel_checkbox,
                                                   variable=self.check_var_video,
                                                   onvalue="on",
                                                   offvalue="off")
        self.checkbox_video.place(relx=0.47, rely=0.4, anchor=tk.CENTER)

        # Create checkbox for Audio
        self.check_var_audio = tk.StringVar(value="")

        self.checkbox_audio = customtkinter.CTkCheckBox(self,
                                                        text="Audio",
                                                        command=self.handel_checkbox,
                                                        variable=self.check_var_audio,
                                                        onvalue="on",
                                                        offvalue="off")
        self.checkbox_audio.place(relx=0.57, rely=0.4, anchor=tk.CENTER)

        # Is combobox for video quality available (initially hidden)
        self.video_quality_combobox = None
        self.qualitimenu = customtkinter.StringVar(value="")

    def download_btn(self):
        url = self.url_entry.get()
        
        if self.checkbox_video.get() == "on":
            # If user want to download Video, it shows quality combobox
            self.create_video_quality_combobox()
            # Pass URL and quality of video
            video_quality = self.video_quality_combobox.get()
            self.download_video_btn(url, video_quality)
            

        elif self.checkbox_audio.get() == "on":
            self.download_audio_btn(url)

        elif self.check_var_audio.get() == "on" and self.checkbox_audio.get() == "on":
            self.download_video_btn(url, self.video_quality_combobox.get())
            self.download_audio_btn(url)

        else:
            self.destroy_video_quality_combobox()

    def handel_checkbox(self):
        if self.check_var_video.get() == "on":
            self.create_video_quality_combobox()
        else: 
            self.destroy_video_quality_combobox()

    def create_video_quality_combobox(self):
        if self.video_quality_combobox is None:
            # Create the combobox
            self.video_quality_combobox = customtkinter.CTkComboBox(
                self,
                values=["High", "Medium", "Low"],
                variable=self.qualitimenu
            )
            self.video_quality_combobox.set("High")
            self.video_quality_combobox.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

    def destroy_video_quality_combobox(self):
        if isinstance(self.video_quality_combobox, None):
            # Destroy combobox
            self.video_quality_combobox.destroy()
            self.video_quality_combobox = None

    def download_video_btn(self, url, video_quality):
        try:
            """Processing .mp4 download"""
            yt = YouTube(url)

            # filter video streams
            video_streams = yt.streams.filter(
                file_extension="mp4",
                resolution=video_quality
            )
            
            if video_streams:
                if video_quality == "High":
                    video = video_streams.get_highest_resolution()
                elif video_quality == "Medium":
                    # Customize based on your requirements
                    # For example, get the medium resolution stream
                    video = video_streams.filter(res="720p").first()
                elif video_quality == "Low":
                    # Customize based on your requirements
                    # For example, get the low resolution stream
                    video = video_streams.filter(res="480p").first()
                else:
                    print("Invalid video quality selection.")
                    return
                
            out_file = video.download()

            download_label = customtkinter.CTkLabel(self,
                                           text="Download complete!",
                                           width=120,
                                           height=25)
            download_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER) 
        except Exception as e:
            raise e

    def download_audio_btn(self, url):
        try:
            """Processing .mp3 download"""
            yt = YouTube(url)

            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            print("success!")
        except Exception as e:
            print(f"An unexpected error occured: {e}")



if __name__ == "__main__":
    app = App()
    app.mainloop()