#!/usr/bin/python

import tkinter as tk
from os import listdir
from os.path import isfile, join
import vlc
import time
import threading
import random

root = tk.Tk()

root.geometry("700x500")
root.resizable(width=0, height=0)
root.configure(background="black")

dir_name = tk.Entry(root, width=30)
dir_name.pack()

current_song = tk.Label(root, text="", height=1, width=100, bg="black", fg="white")
current_song.pack(pady=3)

shuffle_on = tk.Label(root, text="SHUFFLE OFF", height=1, width=15, bg="black", fg="white")
shuffle_on.place(relx=0.1,rely=0.0)

repeat_on = tk.Label(root, text="REPEAT OFF", height=1, width=15, bg="black", fg="white")
repeat_on.place(relx=0.75,rely=0.0)

files_list = []
new_file_list = []

audiofiles = tk.Listbox(root, width=87, height=20, bg="black", fg="white")
audiofiles.place(relx=0.0, rely="0.1")

dead = False
default_shuffle = False
default_repeat = False

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
			return

countdown_thread = threading.Thread(target = wait_test)

def set_play_media():
	global default_shuffle
	countdown_thread = threading.Thread(target = wait_test) 
	media_object.stop()
	
	if(default_repeat == False):
		if(default_shuffle == False):
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
	global default_shuffle
	media_object.stop()
	if(default_shuffle == False):
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
	else:
		random_audio = random.choice(new_file_list) 
		media = vlc.Media(dir_name.get() + "/" + random_audio)
		current_song.configure(text=random_audio)
		media_object.set_media(media)
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

def activate_repeat():
	global default_repeat
	if(default_repeat == False):
		default_repeat = True
		repeat_on.configure(text="REPEAT ON")
	else:
		default_repeat = False
		repeat_on.configure(text="REPEAT OFF")

repeat_option = tk.Button(root, text="REPEAT"+"\n"+"AUDIO", bg="gainsboro", activebackground="gainsboro", command=activate_repeat)
repeat_option.place(rely=0.863, relx=0.56, height=60, width=60)

play_audio = tk.Button(root, text="PLAY"+"\n"+"AUDIO", bg="gainsboro", activebackground="gainsboro", command=play_audio)
play_audio.place(rely=0.863, relx=0.70, height=60, width=60)

choose_dir = tk.Button(root, text="CHOOSE"+"\n"+"DIRECTORY", bg="gainsboro", activebackground="gainsboro", command=list_audio)
choose_dir.place(rely=0.863, relx=0.80, height=60, width=60)

def activate_shuffle():
	global default_shuffle
	if(default_shuffle == False):
		default_shuffle = True
		shuffle_on.configure(text="SHUFFLE ON")
	else:
		shuffle_on.configure(text="SHUFFLE OFF")
		default_shuffle = False

shuffle_audio = tk.Button(root, text="SHUFFLE"+"\n"+"AUDIO", bg="gainsboro", activebackground="gainsboro", command=activate_shuffle)
shuffle_audio.place(rely=0.863, relx=0.90, height=60, width=60)

root.mainloop()
