#!/bin/sh
YOUTUBE_LINK=$1
CLIP_LEN_S=$2

echo $YOUTUBE_LINK
echo $CLIP_LEN_S

rm -rf clip.mp4
youtube-dl -f 'bestvideo[ext=mp4]' --output 'clip.mp4' $YOUTUBE_LINK

# cut the first 5 seconds
ffmpeg -y -loglevel info -i clip.mp4 -t $CLIP_LEN_S video.mp4
# detect poses on the these 5 seconds
rm openpose.avi
cd openpose && ./build/examples/openpose/openpose.bin --video ../video.mp4 --write_json ./output/ --display 0  --write_video ../openpose.avi
# convert the result into MP4
ffmpeg -y -loglevel info -i openpose.avi output.mp4