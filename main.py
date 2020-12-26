import tkinter as tk
from os import listdir
from os.path import isfile, join
import vlc
import time
import threading
import random
import os
from tkinter import *
from tkinter.ttk import *

# create basic tkinter mp3player window
root = tk.Tk()

root.geometry("700x500")
root.resizable(width=0, height=0)
root.title("pyplayer")
root.configure(background="black")

# field to put audiofiles-directory in
dir_name = tk.Entry(root, width=30)
dir_name.pack()

# showing song that is currently playing
current_song = tk.Label(root, text="", height=1, width=100, bg="black", fg="white")
current_song.pack(pady=3)

# text to show if shuffling audiofiles is on or off
shuffle_on = tk.Label(root, text="SHUFFLE OFF", height=1, width=15, bg="black", fg="white")
shuffle_on.place(relx=0.1, rely=0.0)

# text to show if repeating audiofile is on or off
repeat_on = tk.Label(root, text="REPEAT OFF", height=1, width=15, bg="black", fg="white")
repeat_on.place(relx=0.75, rely=0.0)

files_list = []
new_file_list = []

# list that is showing all audiofiles in chosen directory
audiofiles = tk.Listbox(root, width=87, height=20, bg="black", fg="white")
audiofiles.place(relx=0.0, rely="0.1")

# bool to control thread-flow
dead = False

# bool to control if shuffle is on or off
default_shuffle = False

# bool to control if repeating audio is on or off
default_repeat = False


def list_audio():
    """
    list_audio description
    gets all files in chosen directory
    inserts them into audiofiles-list-window
    """

    audiofiles.delete(0, tk.END)
    files_list.clear()
    for i in [f for f in listdir(dir_name.get()) if isfile(join(dir_name.get(), f))]:
        files_list.append(i)
    for i in files_list:
        audiofiles.insert(tk.END, i)


# creating mediaplayer object
media_object = vlc.MediaPlayer()

# setting default value of mediaplayer object
media_object.audio_set_volume(100)


def wait_test():
    """
    wait_test description
    thread that controls when next audiofiles is going to be played
    """
    while True:
        if (str(media_object.get_state()) == "State.Ended"):
            set_play_media()
            return


countdown_thread = threading.Thread(target=wait_test)


def set_play_media():
    """
    set_play_media description
    checks if repeat is on -> plays same audiofile again
    checks if shuffle is on -> plays random audio file using random-module

    plays next audio file normally
    """

    global default_shuffle
    countdown_thread = threading.Thread(target=wait_test)
    media_object.stop()

    if (default_repeat == False):
        if (default_shuffle == False):
            try:
                media = vlc.Media(
                    dir_name.get() + "/" + new_file_list[new_file_list.index(current_song.cget("text")) + 1])
                current_song.configure(text=new_file_list[new_file_list.index(current_song.cget("text")) + 1])
                media_object.set_media(media)
                media_object.play()
            except:
                media = vlc.Media(dir_name.get() + "/" + new_file_list[0])
                current_song.configure(text=new_file_list[0])
                media_object.set_media(media)
                media_object.play()
        else:
            random_audio = random.choice(new_file_list)
            media = vlc.Media(dir_name.get() + "/" + random_audio)
            current_song.configure(text=random_audio)
            media_object.set_media(media)
            media_object.play()
    else:
        media = vlc.Media(dir_name.get() + "/" + current_song.cget("text"))
        media_object.set_media(media)
        media_object.play()
    countdown_thread.start()


def play_audio():
    """
    play_audio description
    plays initial audiofile and sets new-audiofile-list
    """
    global new_file_list
    media_object.stop()
    current_song.configure(text=audiofiles.get(tk.ANCHOR))

    new_file_list = files_list[files_list.index(current_song.cget("text")):] + files_list[:files_list.index(
        current_song.cget("text"))]

    media = vlc.Media(dir_name.get() + "/" + audiofiles.get(tk.ANCHOR))
    media_object.set_media(media)
    media_object.play()
    countdown_thread.start()


def increase_audio():
    media_object.audio_set_volume(media_object.audio_get_volume() + 10)


def decrease_audio():
    media_object.audio_set_volume(media_object.audio_get_volume() - 10)


def next_audio():
    """
    next_audio description
    checks if shuffle is on -> skips to  random audio file as next audio

    skips to next audio file normally
    """
    global default_shuffle
    media_object.stop()
    if (default_shuffle == False):
        try:
            media = vlc.Media(dir_name.get() + "/" + files_list[files_list.index(current_song.cget("text")) + 1])
            media_object.set_media(media)
            current_song.configure(text=files_list[files_list.index(current_song.cget("text")) + 1])
            media_object.play()
        except:
            media = vlc.Media(dir_name.get() + "/" + files_list[0])
            media_object.set_media(media)
            current_song.configure(text=files_list[0])
            media_object.play()
    else:
        random_audio = random.choice(new_file_list)
        media = vlc.Media(dir_name.get() + "/" + random_audio)
        current_song.configure(text=random_audio)
        media_object.set_media(media)
        media_object.play()


def previous_audio():
    """
    previous_audio description
    goes back to previous audiofile in list
    """
    media_object.stop()
    try:
        media = vlc.Media(dir_name.get() + "/" + files_list[files_list.index(current_song.cget("text")) - 1])
        media_object.set_media(media)
        current_song.configure(text=files_list[files_list.index(current_song.cget("text")) - 1])
        media_object.play()
    except:
        media = vlc.Media(dir_name.get() + "/" + files_list[0])
        media_object.set_media(media)
        current_song.configure(text=files_list[files_list.index(current_song.cget("text")) - 1])
        media_object.play()

# create gui-audio-controls
control_audio = tk.Canvas(root, width=697.5, height=75, bg="black")
control_audio.place(rely=0.845, relx=0.0)

go_back_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\go_back.png")

go_back = tk.Button(root, text="", image = go_back_img, command=previous_audio)
go_back.place(rely=0.863, relx=0.02, height=60, width=60)


def pause_audio():
    media_object.pause()

pause_play_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\pause_play.png")
pause_play = tk.Button(root, text="", image = pause_play_img, command=pause_audio)
pause_play.place(rely=0.863, relx=0.12, height=60, width=60)

go_next_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\go_next.png")
go_next = tk.Button(root, text="", image = go_next_img, command=next_audio)
go_next.place(rely=0.863, relx=0.22, height=60, width=60)

volume_down_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\volume_down.png")
volume_down = tk.Button(root, text="", image = volume_down_img, command=decrease_audio)
volume_down.place(rely=0.863, relx=0.32, height=60, width=60)

volume_up_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\volume_up.png")
volume_up = tk.Button(root, text="", image = volume_up_img,command=increase_audio)
volume_up.place(rely=0.863, relx=0.42, height=60, width=60)


def activate_repeat():
    """
    activate_repeat description
    changes repeat text and bool
    """
    global default_repeat
    if (default_repeat == False):
        default_repeat = True
        repeat_on.configure(text="REPEAT ON")
    else:
        default_repeat = False
        repeat_on.configure(text="REPEAT OFF")

repeat_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\repeat_audio.png")
repeat_option = tk.Button(root, text="", image = repeat_img, command=activate_repeat)
repeat_option.place(rely=0.863, relx=0.56, height=60, width=60)

play_audio_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\play_song.png")
play_audio = tk.Button(root, text="", image = play_audio_img, command=play_audio)
play_audio.place(rely=0.863, relx=0.70, height=60, width=60)

choose_dir_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\choose_dir.png")
choose_dir = tk.Button(root, text="", image = choose_dir_img, command=list_audio)
choose_dir.place(rely=0.863, relx=0.80, height=60, width=60)


def activate_shuffle():
    """
    activate_shuffle description
    changes shuffle text and bool
    """
    global default_shuffle
    if (default_shuffle == False):
        default_shuffle = True
        shuffle_on.configure(text="SHUFFLE ON")
    else:
        shuffle_on.configure(text="SHUFFLE OFF")
        default_shuffle = False

shuffle_audio_img = PhotoImage(file = r"C:\Users\Aytur\PycharmProjects\Pyplayer\shuffle_audio.png")
shuffle_audio = tk.Button(root, text="", image = shuffle_audio_img, command=activate_shuffle)
shuffle_audio.place(rely=0.863, relx=0.90, height=60, width=60)

root.mainloop()