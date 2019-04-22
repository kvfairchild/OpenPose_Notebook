#!/bin/sh
VIDEO_PATH=$1
CLIP_START=$2
CLIP_END=$3

rm -rf clip.mp4

if [ -f $VIDEO_PATH ]
then
	mv $VIDEO_PATH 'clip.mp4'
else
	youtube-dl -f 'bestvideo[ext=mp4]' --output 'clip.mp4' $VIDEO_PATH
fi

# cut the first n seconds
ffmpeg -y -loglevel info -i 'clip.mp4' -ss $CLIP_START -to $CLIP_END -async 1 -strict -2 video.mp4
# detect poses on the these n seconds
rm openpose.avi
cd openpose && ./build/examples/openpose/openpose.bin --net_resolution '1312x736' --scale_number 4 --scale_gap 0.25  --hand --hand_scale_number 6 --hand_scale_range 0.4 --face --video ../video.mp4 --write_json ./output/ --display 0  --write_video ../openpose.avi
# convert the result into MP4
ffmpeg -y -loglevel info -i ../openpose.avi output.mp4

echo "OpenPose video processing complete."