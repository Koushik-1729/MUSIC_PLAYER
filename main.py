import tkinter as tk
import pygame
import os
import random
from mutagen.mp3 import MP3


# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()


window = tk.Tk()
window.title("Music Player")


window.geometry("600x750")
window.configure(bg="#FFCCFF")

MUSIC_DIRECTORY = "D:/music"
music_files = os.listdir(MUSIC_DIRECTORY)

current_song_index = 0


volume = 0.5


shuffle_mode = False
repeat_mode = False


def play_song():
    pygame.mixer.music.load(os.path.join(MUSIC_DIRECTORY, music_files[current_song_index]))
    pygame.mixer.music.play()
    update_song_info()
    update_progress()


def pause_song():
    pygame.mixer.music.pause()


def unpause_song():
    pygame.mixer.music.unpause()


def stop_song():
    pygame.mixer.music.stop()
    progress_slider.set(0)  # Reset the progress slider

# This is Function to play the next song
def next_song(event=None):
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(music_files) - 1)
    else:
        current_song_index = (current_song_index + 1) % len(music_files)
    play_song()

def prev_song(event=None):
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(music_files) - 1)
    else:
        current_song_index = (current_song_index - 1) % len(music_files)
    play_song()


def update_song_info():
    song_info_label.config(text="Now Playing: " + music_files[current_song_index])
    update_song_duration()


def update_song_duration():
    song_path = os.path.join(MUSIC_DIRECTORY, music_files[current_song_index])
    audio = MP3(song_path)
    duration = audio.info.length
    duration_label.config(text="Duration: {:.2f}".format(duration/60))

# Function to update the progress bar/slider
def update_progress():
    song_length = pygame.mixer.music.get_length()
    current_time = pygame.mixer.music.get_pos() / 1000
    progress_percentage = (current_time / song_length) * 100
    progress_slider.set(progress_percentage)
    window.after(1000, update_progress)  

def seek_song(event):
    song_length = pygame.mixer.music.get_length()
    seek_time = (progress_slider.get() / 100) * song_length
    pygame.mixer.music.set_pos(seek_time / 1000)

# Function to decrease volume
def decrease_volume():
    global volume
    if volume > 0.1:
        volume -= 0.1
        pygame.mixer.music.set_volume(volume)

# Function to increase volume
def increase_volume():
    global volume
    if volume < 1.0:
        volume += 0.1
        pygame.mixer.music.set_volume(volume)


def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode

# Create the play button
play_button = tk.Button(window, text="Play", command=play_song, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
play_button.pack(pady=10)

# Create the pause button
pause_button = tk.Button(window, text="Pause", command=pause_song, bg="#ff9800", fg="white", font=("Arial", 12, "bold"))
pause_button.pack(pady=5)

# Create the unpause button
unpause_button = tk.Button(window, text="Unpause", command=unpause_song, bg="#ff9800", fg="white", font=("Arial", 12, "bold"))
unpause_button.pack(pady=5)

# Create the stop button
stop_button = tk.Button(window, text="Stop", command=stop_song, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
stop_button.pack(pady=5)

# Create the next button
next_button = tk.Button(window, text="Next", command=next_song, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
next_button.pack(pady=5)

# Create the previous button
prev_button = tk.Button(window, text="Previous", command=prev_song, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
prev_button.pack(pady=5)

# Create the song information label
song_info_label = tk.Label(window, text="", font=("Arial", 12))
song_info_label.pack(pady=10)

# Create the duration label
duration_label = tk.Label(window, text="Duration: ", font=("Arial", 12))
duration_label.pack(pady=5)

# Create the volume control buttons
volume_label = tk.Label(window, text="Volume", font=("Arial", 12))
volume_label.pack(pady=5)

decrease_volume_button = tk.Button(window, text="-", command=decrease_volume, bg="#9e9e9e", fg="white", font=("Arial", 12, "bold"))
decrease_volume_button.pack(pady=5)

increase_volume_button = tk.Button(window, text="+", command=increase_volume, bg="#9e9e9e", fg="white", font=("Arial", 12, "bold"))
increase_volume_button.pack(pady=5)

# Create the shuffle checkbox
shuffle_checkbox = tk.Checkbutton(window, text="Shuffle", command=toggle_shuffle, bg="#f0f0f0", font=("Arial", 12))
shuffle_checkbox.pack(pady=5)

# Create the repeat checkbox
repeat_checkbox = tk.Checkbutton(window, text="Repeat", command=toggle_repeat, bg="#f0f0f0", font=("Arial", 12))
repeat_checkbox.pack(pady=5)

window.bind("<space>", pause_song)  # Spacebar for play/pause
window.bind("<Right>", next_song)  # Right arrow key for next song
window.bind("<Left>", prev_song)   # Left arrow key for previous song

window.mainloop()

# end of pygame
pygame.quit()
