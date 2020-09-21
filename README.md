# *Pyplayer*

## An open source audio player
This is an open source audio-file player built with python and various libraries, use it however you want.

## How to build

Dependencies:
- any Python3 version 
- Tkinter, vlc, PIL modules

How to install modules:
```
pip3 install Tkinter
pip3 install python-vlc
pip3 install pil 
```

If any linux users get "ImportError: cannot import name 'ImageTK' ", try:
```
Debian/Ubuntu: sudo apt-get install python3-pil python3-pil.imagetk
Archlinux: sudo pacman -S python-pillow or sudo pacman -S python-pillow
```

If any windows users get an ImportError, try:
```
pip3 install pillow
```
## How to use
Copy the directory-path of the directory (where all your audiofiles are) into the input field inside the program, after that click the second button from right to load the directory into the program. Now you can select any song you want and play it with the play button. All the audiofiles inside the directory will play like a normal playlist. (You can shuffle and repeat a specified audiofile aswell)
