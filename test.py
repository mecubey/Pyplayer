import vlc
import time

audio_path = "/home/cubybros/repos/python_audioplayer/sample_audio/y2mate.com - Duck Army_nHc288IPFzk.mp3"

media = vlc.Media(audio_path)
player = vlc.MediaPlayer()
player.set_media(media)
player.play()

while (str(player.get_state()) != "State.Ended"):
	print(str(player.get_state()))
