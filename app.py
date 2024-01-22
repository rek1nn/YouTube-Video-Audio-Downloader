"""
Last update: 22.01.2024
Developed by: 
https://github.com/rek1nn
https://t.me/valikmm
"""

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
        self.geometry(f"{1100}x{580}")

        # Create an entry field for URL
        self.url_var = tk.StringVar()
        self.url_entry = customtkinter.CTkEntry(self,
                                               textvariable=self.url_var,
                                               width=475,
                                               height=30)
        self.url_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Home directory of user. Example: C:\Users\Pro
        self.USER_HOME_DIRECTORY = os.path.expanduser("~")
        self.USER_DOWNLOAD_DIRECTORY = os.path.join(self.USER_HOME_DIRECTORY, "Downloads")

        # Create download button
        self.btn = customtkinter.CTkButton(
            self, text="Download", command=self.download_btn
        )
        self.btn.place(relx=0.5, rely=0.49, anchor=tk.CENTER)

        # Create checkbox for video
        self.check_var_video = tk.StringVar(value="")

        self.checkbox_video = customtkinter.CTkCheckBox(self,
                                                   text="Video",
                                                   command=self.handel_checkbox,
                                                   variable=self.check_var_video,
                                                   onvalue="on",
                                                   offvalue="off")
        self.checkbox_video.place(relx=0.47, rely=0.4, anchor=tk.CENTER)

        # Create checkbox for audio
        self.check_var_audio = tk.StringVar(value="")

        self.checkbox_audio = customtkinter.CTkCheckBox(self,
                                                        text="Audio",
                                                        command=self.handel_checkbox,
                                                        variable=self.check_var_audio,
                                                        onvalue="on",
                                                        offvalue="off")
        self.checkbox_audio.place(relx=0.57, rely=0.4, anchor=tk.CENTER)

        # Combobox for video quality (initially hidden)
        self.video_quality_combobox = None
        self.qualitimenu = customtkinter.StringVar(value="")

        # Progress bar
        self.progress_label = customtkinter.CTkLabel(self, text="0%")
        
        self.progress_bar = customtkinter.CTkProgressBar(self, width=400)

        # Create the status label
        self.status = customtkinter.CTkLabel(self, text="", width=120, height=25)

        #Load the image
        self.image_path = "Youloader.png"
        self.image = PhotoImage(file=self.image_path)

        # Adjust the size (change the factors as needed)
        self.image = self.image.subsample(5, 5)  # Change the factors according to your needs

        # Create a label for the image
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.image_label.place(relx=0.16, rely=0.12, anchor=tk.CENTER)

    def download_btn(self):
        url = self.url_entry.get()
        
        if self.checkbox_video.get() == "on":
            # If user want to download Video, it shows quality combobox
            self.create_video_quality_combobox()
            # Pass URL and quality of video
            video_quality = self.video_quality_combobox.get()
            self.download_video_btn(url)
        
        elif self.checkbox_audio.get() == "on":
            self.download_audio_btn(url)
        
        # If both was clicked
        elif self.check_var_audio.get() == "on" and self.checkbox_audio.get() == "on":
            self.download_video_btn(url)
            self.download_audio_btn(url)
        
        else:
            self.destroy_video_quality_combobox()

    def handel_checkbox(self):
        # If checkbox Video clicked, show quality opportunities
        if self.check_var_video.get() == "on":
            self.create_video_quality_combobox()
        else: 
            self.destroy_video_quality_combobox()

    def create_video_quality_combobox(self):
        if self.video_quality_combobox is None:
            # Create combobox for quality
            self.video_quality_combobox = customtkinter.CTkComboBox(
                self,
                values=["High", "Low"],
                variable=self.qualitimenu
            )
            self.video_quality_combobox.place(relx=0.34, rely=0.4, anchor=tk.CENTER)

    def destroy_video_quality_combobox(self):
        if self.video_quality_combobox is not None:
            # Destroy combobox
            self.video_quality_combobox.destroy()
            self.video_quality_combobox = None

    def download_audio_btn(self, url):
        """Processing .mp3 download"""  
        # Place the status
        self.status.place(relx=0.5, rely=0.62, anchor=tk.CENTER)
        # Create YouTube class
        yt = YouTube(url, on_progress_callback=self.on_progress)
        # Direction to file 
        title = yt.title
        video_name = title + ".mp3"
        dir = os.path.join(self.USER_DOWNLOAD_DIRECTORY, video_name)
        
        try:
            stream = yt.streams.filter(only_audio=True).first()
            
            if stream:
                # Place the progress bar 
                self.progress_label.place(relx=0.75, rely=0.56, anchor=tk.CENTER)
                self.progress_bar.place(relx=0.5, rely=0.56, anchor=tk.CENTER)
                self.progress_bar.set(0)
                
                #  Download file and convert to .mp3
                out_file = stream.download(self.USER_DOWNLOAD_DIRECTORY)
                base, ext = os.path.splitext(out_file)
                new_file = base + ".mp3"
                os.rename(out_file, new_file)

                # Update status text
                self.status.configure(
                        text=f"Download complete!\nYour file is located in the following directory: {dir}", text_color="green")
            else: 
                raise Exception
        except Exception as e:
            # Update status text to the error message with red color
            self.status.configure(text=str(e), text_color="red")

    def download_video_btn(self, url):        
        """Processing .mp4 download"""
        
        # Place the status
        self.status.place(relx=0.5, rely=0.62, anchor=tk.CENTER)
        # Create YouTube class
        yt = YouTube(url, on_progress_callback=self.on_progress)
        # Direction to file 
        title = yt.title
        video_name = title + ".mp4"
        dir = os.path.join(self.USER_DOWNLOAD_DIRECTORY, video_name)
        
        try:
            if self.video_quality_combobox is not None:
                video_quality = self.video_quality_combobox.get()
                
                """Choose quality"""
                if video_quality == "High":
                    stream = yt.streams.get_highest_resolution()

                elif video_quality == "Low":
                    stream = yt.streams.get_lowest_resolution()

                if stream:
                    # Show progressbar and status
                    self.progress_label.place(relx=0.75, rely=0.56, anchor=tk.CENTER)
                    self.progress_bar.place(relx=0.5, rely=0.56, anchor=tk.CENTER)
                    self.progress_bar.set(0)

                    stream.download(self.USER_DOWNLOAD_DIRECTORY)
                    # Update status text
                    self.status.configure(
                        text=f"Download complete!\nYour file is located in the following directory: {dir}", text_color="green")
        except Exception as e:
            # Update status text to the error message with red color
            self.status.configure(text=str(e), text_color="red")
            print(e)

    def on_progress(self, stream, chunk, bytes_remaining):
        # Calculation
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        precentage_completed = bytes_downloaded / total_size * 100

        # Convert bytes to megabytes
        total_size_MB = total_size / (1024 * 1024)
        bytes_downloaded_MB = bytes_downloaded / (1024 * 1024)

        # Display downloaded and total size in megabytes
        b = f"{bytes_downloaded_MB:.2f}MB / {total_size_MB:.2f}MB"

        # Visual updating
        self.progress_label.configure(text=b)
        self.progress_bar.update()
        self.progress_bar.set(float(precentage_completed / 100))


if __name__ == "__main__":
    app = App()
    app.mainloop()