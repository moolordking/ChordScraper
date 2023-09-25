import tkinter as tk
from tkinter import ttk
import bin.scraper as sr

def process_line(lines, index, length, progress_bar, root):
    if index >= length:
        root.quit()  # Close the GUI when the catalog is complete
        return

    l = lines[index]
    if len(l) > 45:
        l = l[0:45]
    res = sr.scrape_chords(l, False, False)

    divby = length / 100

    if divby != 0 and int(index % divby) == 0:
        update_progress(progress_bar, index / length * 100, root)

    # Call the function recursively for the next line
    process_line(lines, index + 1, length, progress_bar, root)

def update_progress(progress_bar, value, root):
    progress_bar["value"] = value
    root.update_idletasks()

def start_catalogue():
    root = tk.Tk()
    root.title("Song Catalogue Progress")
    root.configure(bg="#EEF")  # Set the background color

    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=20)

    style = ttk.Style()
    style.configure("TButton", font=("Courier", 12), foreground="#222", background="white", borderwidth=0)
    style.map("TButton", background=[("active", "white")])
    style.configure("TProgressbar", background="#EEF", troughcolor="#EEF")
    style.map("TProgressbar", background=[("active", "purple")])

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
    progress_bar.grid(row=0, column=0, padx=5, pady=5)

    start_button = ttk.Button(frame, text="Start Catalogue", command=lambda: catalogue(progress_bar, root), style="TButton")
    start_button.grid(row=1, column=0, padx=5, pady=5)

    root.mainloop()

def catalogue(progress_bar, root):
    with open("SONGS.txt") as f:
        lines = f.readlines()
        length = len(lines)
        progress_bar["maximum"] = 100  # Set the maximum value of the progress bar
        process_line(lines, 0, length, progress_bar, root)