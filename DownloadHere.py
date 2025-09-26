import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path


#Text updates in GUI
class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END) # Auto-scroll to the end

    def flush(self):
        pass # Required for file-like objects

root = tk.Tk()
root.title("YTD")
root.geometry("400x160")  # set the window size to 400x160

droppoint = Path.home() / "Downloads" / "Video Downloads" # Video destination (fixed to Downloads folder now)
print(droppoint)

def run_youtube_dl(input_url):
    if not os.path.exists(droppoint):
        os.makedirs(droppoint)

    print("Starting")
    output_path = os.path.join(droppoint, "%(title)s.%(ext)s")
    cmd = f'yt-dlp.exe -vU -f best -o "{output_path}" -P {os.path.join(droppoint)} "{input_url}"'

    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        show_finish_window()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def show_finish_window():
    # Show the finish window
    finish = tk.Toplevel(root)
    finish.geometry("200x160")
    finish.title("Done")

    finish_label = tk.Label(finish, text="Done")
    finish_label.pack()

    # Create an "OK" button to close the finish window
    ok_button = tk.Button(finish, text="OK", command=finish.destroy)
    ok_button.pack()

def update_ytdl():
    print("Starting Update")
    cmd = "yt-dlp.exe -U -vU --no-check-certificate"

    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def open_folder():
    print("opening download folder")
    if not os.path.exists(droppoint):
        os.makedirs(droppoint)
    os.startfile(droppoint)  # download folder

# Create a label and text box for the input URL, and move the download button beside it
url_frame = tk.Frame(root)
url_frame.pack()

url_label = tk.Label(url_frame, text="Enter YouTube URL:")
url_label.pack(side=tk.LEFT)

url_entry = tk.Entry(url_frame)
url_entry.pack(side=tk.LEFT, padx=5)

# Create a button to trigger the download
run_button = tk.Button(url_frame, text="Download", command=lambda: run_youtube_dl(url_entry.get()))
run_button.pack(side=tk.RIGHT)

# Create a button to update yt-dlp
update_button = tk.Button(root, text="Update YTDL", command=update_ytdl)
update_button.pack(pady=5)

# Create a button to open the destination folder
open_button = tk.Button(root, text="Open Folder", command=open_folder)
open_button.pack(pady=5)

# Create a Text widget for displaying output
output_text = tk.Text(root, wrap='word', height=15, width=60)
output_text.pack(padx=10, pady=10)

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

# Redirect sys.stdout to the custom ConsoleRedirector
sys.stdout = ConsoleRedirector(output_text)

root.mainloop()
