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

		return display_local(video_path)


def display_local(video_path, width=640, height=480):
 
	import io
	import base64
	from IPython.display import HTML

	video_encoded = base64.b64encode(io.open(video_path, 'rb').read())

	return HTML(data='''<video width="{0}" height="{1}" alt="test" controls>
	                <source src="data:video/mp4;base64,{2}" type="video/mp4" />
	              </video>'''.format(width, height, video_encoded.decode('ascii')))


def openpose_installed():

	import os
	from os.path import splitext, basename, exists

	git_repo_url = 'https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
	project_name = splitext(basename(git_repo_url))[0]

	if exists(project_name):
		print("Existing OpenPose installation detected, moving on.")
		return True
	else:
		return False


def _get_id_from_link(YOUTUBE_LINK):

	prefix, YOUTUBE_ID = YOUTUBE_LINK.split("=")

	return YOUTUBE_ID
