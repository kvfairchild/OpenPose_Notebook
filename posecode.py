# Functions to abstract OpenPose.ipynb logic


def is_valid_youtube(YOUTUBE_LINK):
  
  import json
  import requests
  
  youtube_url = "https://www.youtube.com/oembed?format=json&url=" + YOUTUBE_LINK
  
  try:
    r = requests.head(youtube_url)
    if r.status_code == 200:
      return True
    else:
      return False
    
  except requests.ConnectionError:
    print("Failed to connect to YouTube.")
    return False


def display_video(video_path, youtube):

	if youtube:

		from IPython.display import YouTubeVideo, HTML

		# display video
		YOUTUBE_ID = _get_id_from_link(video_path)

		video = YouTubeVideo(YOUTUBE_ID)
		display(video)

	else:

		display_local(video_path)


def display_local(video_path, width=640, height=480):
 
  import io
  import base64
  from IPython.display import HTML
 
  video_encoded = base64.b64encode(io.open(video_path, 'rb').read())
 
  return HTML(data='''<video width="{0}" height="{1}" alt="test" controls>
                        <source src="data:video/mp4;base64,{2}" type="video/mp4" />
                      </video>'''.format(width, height, video_encoded.decode('ascii')))


def run_openpose(video):

	import os

	os.system("!rm -rf clip.mp4")
	os.system("!youtube-dl -f 'bestvideo[ext=mp4]' --output 'clip.mp4' $YOUTUBE_LINK")

	# cut the first 5 seconds
	os.system("!ffmpeg -y -loglevel info -i clip.mp4 -t $CLIP_LEN_S video.mp4")
	# detect poses on the these 5 seconds
	os.system("!rm openpose.avi")
	os.system("!cd openpose && ./build/examples/openpose/openpose.bin --video ../video.mp4 --write_json ./output/ --display 0  --write_video ../openpose.avi")
	# convert the result into MP4
	os.system("!ffmpeg -y -loglevel info -i openpose.avi output.mp4")



def _get_id_from_link(YOUTUBE_LINK):

	prefix, YOUTUBE_ID = YOUTUBE_LINK.split("=")

	return YOUTUBE_ID
