#!/usr/bin/python

import tkinter as tk
root = tk.Tk()

root.geometry("700x500")
root.resizable(width=0, height=0)
root.configure(background="black")

control_audio = tk.Canvas(root, width=697.5, height=75, bg="black")
control_audio.place(rely=0.845, relx=0.0)

go_back = tk.Button(root, text="GO"+"\n"+"BACK", bg="#1D1D1F", activebackground="#1D1D1F")
go_back.place(rely=0.863, relx=0.02, height=60, width=60)

pause_play = tk.Button(root, text="PLAY/"+"\n"+"PAUSE", bg="#1D1D1F", activebackground="#1D1D1F")
pause_play.place(rely=0.863, relx=0.12, height=60, width=60)

go_next = tk.Button(root, text="GO"+"\n"+"NEXT", bg="#1D1D1F", activebackground="#1D1D1F")
go_next.place(rely=0.863, relx=0.22, height=60, width=60)

root.mainloop()
