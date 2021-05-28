import pafy
import vlc
import os
import time

url = "https://www.youtube.com/watch?v=bMt47wvK6u0"

video = pafy.new(url)
best = video.getbest()
playurl = best.url

skipTime = 1000*10*10 # milliseconds


directory = "images/"
prefix = str.split(url, "=")[1] + "_" # get video ID, end of url
harvesting = False
waitForBuffer = False
recordTime = 0

def callbackBuffering(arg):
    global waitForBuffer
    global harvesting

    if(recordTime + skipTime < arg.u.new_time and harvesting):
        waitForBuffer = False

try:
    os.mkdir("images")
except:
    print("directory exists")    


Instance = vlc.Instance()
player = Instance.media_player_new()
eventManager = player.event_manager()
eventManager.event_attach(vlc.EventType.MediaPlayerBuffering, callback = callbackBuffering)



Media = Instance.media_new(playurl)
Media.get_mrl()
player.set_media(Media)

player.play()

time.sleep(5) # wait till the window appears
player.pause()

images = 0
harvesting = True
while(player.get_time() < player.get_length()):

    waitForBuffer = True
    path = directory + prefix + str(player.get_time() )
    print("image will be taken at " + str(player.get_time() ) + "ms at path "+ path )   
    time.sleep(0.5)
    recordTime = player.get_time()
    player.video_take_snapshot(0, directory + prefix + str(recordTime) ,i_width=player.video_get_width(), i_height=player.video_get_height())

    player.set_time(recordTime+skipTime)



    while(waitForBuffer):
        print("waiting for buffering")
        time.sleep(0.1)