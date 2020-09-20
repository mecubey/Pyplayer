#!/usr/bin/python

import tkinter as tk
from os import listdir
from os.path import isfile, join
import vlc
import time
import threading

root = tk.Tk()

root.geometry("700x500")
root.resizable(width=0, height=0)
root.configure(background="black")

dir_name = tk.Entry(root, width=30)
dir_name.pack()

current_song = tk.Label(root, text="", height=1, width=100, bg="black", fg="white")
current_song.pack(pady=3)

files_list = []
new_file_list = []

audiofiles = tk.Listbox(root, width=87, height=20, bg="black", fg="white")
audiofiles.place(relx=0.0, rely="0.1")

dead = False

def list_audio():
	audiofiles.delete(0, tk.END)
	for i in [f for f in listdir(dir_name.get()) if isfile(join(dir_name.get(), f))]:
		files_list.append(i)
	for i in files_list:
		audiofiles.insert(tk.END, i)

media_object = vlc.MediaPlayer()
media_object.audio_set_volume(100)

def wait_test():
	while True:
		if(str(media_object.get_state()) == "State.Ended"):
			set_play_media()
			print("lol")
			return

countdown_thread = threading.Thread(target = wait_test)

def set_play_media():
	countdown_thread = threading.Thread(target = wait_test) 
	media_object.stop()
	try:
		media = vlc.Media(dir_name.get() + "/" + new_file_list[new_file_list.index(current_song.cget("text"))+1])
		current_song.configure(text=new_file_list[new_file_list.index(current_song.cget("text"))+1])
		media_object.set_media(media)
		media_object.play()
	except:
		media = vlc.Media(dir_name.get() + "/" + new_file_list[0])
		current_song.configure(text=new_file_list[0])
		media_object.set_media(media)
		media_object.play()
		
	countdown_thread.start()

def play_audio():
	global new_file_list
	media_object.stop()
	current_song.configure(text=audiofiles.get(tk.ANCHOR))
	
	new_file_list = files_list[files_list.index(current_song.cget("text")):] + files_list[:files_list.index(current_song.cget("text"))] 
	
	media = vlc.Media(dir_name.get() + "/" + audiofiles.get(tk.ANCHOR))
	media_object.set_media(media)
	media_object.play()
	countdown_thread.start()

def pause_audio():
	media_object.pause()

def increase_audio():
	media_object.audio_set_volume(media_object.audio_get_volume()+10)

def decrease_audio():
	media_object.audio_set_volume(media_object.audio_get_volume()-10)

def next_audio():
	media_object.stop()
	try:
		media = vlc.Media(dir_name.get() + "/" + files_list[files_list.index(current_song.cget("text"))+1])
		media_object.set_media(media)
		current_song.configure(text=files_list[files_list.index(current_song.cget("text"))+1])
		media_object.play()
	except:
		media = vlc.Media(dir_name.get() + "/" + files_list[0])
		media_object.set_media(media)
		current_song.configure(text=files_list[0])
		media_object.play()


def previous_audio():
	media_object.stop()
	try:
		media = vlc.Media(dir_name.get() + "/" + files_list[files_list.index(current_song.cget("text"))-1])
		media_object.set_media(media)
		current_song.configure(text=files_list[files_list.index(current_song.cget("text"))-1])
		media_object.play()
	except:
		media = vlc.Media(dir_name.get() + "/" + files_list[0])
		media_object.set_media(media)
		current_song.configure(text=files_list[files_list.index(current_song.cget("text"))-1])
		media_object.play()


control_audio = tk.Canvas(root, width=697.5, height=75, bg="black")
control_audio.place(rely=0.845, relx=0.0)

go_back = tk.Button(root, text="GO"+"\n"+"BACK", bg="gainsboro", activebackground="gainsboro", command=previous_audio)
go_back.place(rely=0.863, relx=0.02, height=60, width=60)

pause_play = tk.Button(root, text="PLAY/"+"\n"+"PAUSE", bg="gainsboro", activebackground="gainsboro", command=pause_audio)
pause_play.place(rely=0.863, relx=0.12, height=60, width=60)

go_next = tk.Button(root, text="GO"+"\n"+"NEXT", bg="gainsboro", activebackground="gainsboro", command=next_audio)
go_next.place(rely=0.863, relx=0.22, height=60, width=60)

volume_down = tk.Button(root, text="VOLUME"+"\n"+"DOWN", bg="gainsboro", activebackground="gainsboro", command=decrease_audio)
volume_down.place(rely=0.863, relx=0.32, height=60, width=60)

volume_up = tk.Button(root, text="VOLUME"+"\n"+"UP", bg="gainsboro", activebackground="gainsboro", command=increase_audio)
volume_up.place(rely=0.863, relx=0.42, height=60, width=60)

play_audio = tk.Button(root, text="PLAY"+"\n"+"AUDIO", bg="gainsboro", activebackground="gainsboro", command=play_audio)
play_audio.place(rely=0.863, relx=0.62, height=60, width=60)

choose_dir = tk.Button(root, text="CHOOSE"+"\n"+"DIRECTORY", bg="gainsboro", activebackground="gainsboro", command=list_audio)
choose_dir.place(rely=0.863, relx=0.72, height=60, width=60)

shuffle_audio = tk.Button(root, text="SHUFFLE"+"\n"+"AUDIO", bg="gainsboro", activebackground="gainsboro")
shuffle_audio.place(rely=0.863, relx=0.82, height=60, width=60)

root.mainloop()
