import vlc
import os 
os.add_dll_directory('D:/Program Files/VideoLAN/VLC')
import pafy
import time
url = "https://www.youtube.com/watch?v=iZwWlCqezjM"
start = 10
stop = 15
video = pafy.new(url)
best = video.getbest()
playurl = best.url
instance = vlc.Instance()
player=instance.media_player_new() 
media=instance.media_new(playurl) 
start_str = 'start-time=' + str(start)
stop_str = 'stop-time=' + str(stop)
media.add_option(start_str)
media.add_option(stop_str) 

media.get_mrl() 
player.set_media(media) 
player.play() 
time.sleep(50) 