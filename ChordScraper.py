import tkinter as tk
import tkinter.ttk as ttk
import ctypes
import bin.scraper as sr
import bin.Get_Random_Song as grs
import bin.get_from_spotify as gfs
import bin.Many_Scraper as ms

def input_entered():
    input_text = entry.get()
    entry.delete(0, tk.END)
    sr.scrape_chords(input_text, True)

def randomize_entered():
    grs.open_random()

def open_playlist_conversion_window():
    # Create a new window for playlist conversion
    playlist_window = tk.Toplevel(root)
    playlist_window.geometry("800x400")
    playlist_window.title("Convert Spotify Playlist")
    playlist_window.configure(bg="#EEF")

    # Create a title label in the playlist window
    title_label = tk.Label(playlist_window, text="Enter the Spotify playlist URL:", font=("Courier", 14), fg="#222", bg="#EEF")
    title_label.place(relx=0.5, rely=0.3, anchor="center")

    # Create an input box in the playlist window
    playlist_entry = ttk.Entry(playlist_window, font=("Courier", 16), style='TEntry', foreground="#222")
    playlist_entry.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)

    # Create a "Submit" button in the playlist window
    def submit_playlist():
        playlist_url = playlist_entry.get()
        playlist_window.destroy()  # Close the playlist window
        try:
        	gfs.locate_and_add_playlist(playlist_url)
        	ms.start_catalogue()
        except Exception as e:
        	print(f"An error occurred: {str(e)}")

    submit_button = tk.Button(playlist_window, text="Submit", font=("Courier", 14), bg="white", fg="#222", command=submit_playlist, bd=0, cursor="hand2")
    submit_button.place(relx=0.5, rely=0.6, anchor="center")

# Get screen width and height
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Calculate the center of the screen
window_width = 1000
window_height = 600
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Create the main window with the title 'ChordScraper'
root = tk.Tk()
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#EEF")
root.title("ChordScraper")  # Set the window title

# Create a title label with monospaced font
title_label = tk.Label(root, text="Enter a song and artist to find the corresponding chords", font=("Courier", 14), fg="#222", bg="#EEF")
title_label.place(relx=0.5, rely=0.3, anchor="center")

# Create an input box with monospaced font and a spread-out drop shadow
entry_style = ttk.Style()
entry_style.configure('TEntry', padding=10, relief="ridge", borderwidth=3)
entry = ttk.Entry(root, font=("Courier", 16), style='TEntry', foreground="#222")
entry.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)

# Create a "Submit" button without a border with monospaced font and a pointer cursor
submit_button = tk.Button(root, text="Submit", font=("Courier", 14), bg="white", fg="#222", command=input_entered, bd=0, cursor="hand2")
submit_button.place(relx=0.35, rely=0.5, anchor="center")

# Create a "Randomize" button with a randomize symbol with monospaced font and a pointer cursor
randomize_button = tk.Button(root, text="Randomize", font=("Courier", 14), bg="white", fg="#222", command=randomize_entered, bd=0, cursor="hand2")
randomize_button.place(relx=0.65, rely=0.5, anchor="center")

# Create a "Convert Spotify Playlist" button
playlist_button = tk.Button(root, text="Convert Spotify Playlist", font=("Courier", 14), bg="white", fg="#222", command=open_playlist_conversion_window, bd=0, cursor="hand2")
playlist_button.place(relx=0.5, rely=0.65, anchor="center")

# Bind the Enter key to trigger the input_entered function
root.bind("<Return>", lambda event=None: input_entered())

root.mainloop()
