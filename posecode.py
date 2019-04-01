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
      print("Please enter a valid YouTube URL.")
      return False
    
  except requests.ConnectionError:
    print("Failed to connect.")
    return False


def install_openpose():

	import os
	from os.path import splitext, basename, exists

	git_repo_url = 'https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
	project_name = splitext(basename(git_repo_url))[0]

	if not exists(project_name):

	  # see: https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/949
	  # install new CMake becaue of CUDA10
	  os.system("!wget -q https://cmake.org/files/v3.13/cmake-3.13.0-Linux-x86_64.tar.gz")
	  os.system("!tar xfz cmake-3.13.0-Linux-x86_64.tar.gz --strip-components=1 -C /usr/local")
	  # clone openpose
	  os.system("!git clone -q --depth 1 $git_repo_url")
	  os.system("!sed -i 's/execute_process(COMMAND git checkout master WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/execute_process(COMMAND git checkout f019d0dfe86f49d1140961f8c7dec22130c83154 WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/g' openpose/CMakeLists.txt")
	  # install system dependencies
	  os.system("!apt-get -qq install -y libatlas-base-dev libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev opencl-headers ocl-icd-opencl-dev libviennacl-dev")
	  # install python dependencies
	  os.system("!pip install -q youtube-dl")
	  # build openpose
	  os.system("!cd openpose && rm -rf build || true && mkdir build && cd build && cmake .. && make -j`nproc`")


def display_video(video):

	from IPython.display import YouTubeVideo, HTML

	if type(video) == str:

		YOUTUBE_ID = get_id_from_link(video)

		vid = YouTubeVideo(YOUTUBE_ID)
		display(vid)

		youtube_download(YOUTUBE_ID)

	else:

		import io
		import base64

		video = io.open(video, 'r+b').read()
		encoded = base64.b64encode(video)
		HTML(data='''<video alt="test" controls>
		                <source src="data:video/mp4;base64,{0}" type="video/mp4" />
		             </video>'''.format(encoded.decode('ascii')))


def youtube_download(YOUTUBE_ID):

	import os

	print("YES")

	youtube_url = 'https://www.youtube.com/watch?v=' + YOUTUBE_ID
	print(youtube_url)

	os.system("!youtube-dl -f 'bestvideo[ext=mp4]' --output 'clip.%(ext)s' $youtube_url")



def get_id_from_link(YOUTUBE_LINK):

	prefix, YOUTUBE_ID = YOUTUBE_LINK.split("=")

	return YOUTUBE_ID
