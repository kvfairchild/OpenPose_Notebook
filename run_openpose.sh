#!/bin/sh
VIDEO_PATH=$1
CLIP_START=$2
CLIP_END=$3

rm -rf clip.mp4

if [-f $VIDEO_PATH]
then
	echo '$VIDEO_PATH is a file'
	mv '$VIDEO_PATH' 'clip.mp4'
else
	echo '$VIDEO_PATH is not a file'
	youtube-dl -f 'bestvideo[ext=mp4]' --output 'clip.mp4' $VIDEO_PATH
fi

# cut the first n seconds
ffmpeg -y -loglevel info -i $VIDEO_PATH -ss $CLIP_START -to $CLIP_END -async 1 -strict -2 video.mp4
# detect poses on the these n seconds
rm openpose.avi
cd openpose && ./build/examples/openpose/openpose.bin --video ../video.mp4 --write_json ./output/ --display 0  --write_video ../openpose.avi
# convert the result into MP4
ffmpeg -y -loglevel info -i ../openpose.avi output.mp4

echo "OpenPose video processing complete."