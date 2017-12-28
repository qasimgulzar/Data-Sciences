
for f in *.mp4; do ffmpeg -r 30 -i $f -vf scale=640:360 -c:v libx264 -crf 18 -preset medium -c:a copy encoded/encoded-$f;done
rm list.txt
for f in encoded/encoded-*.mp4; do echo "file '$(pwd)/$f'">>list.txt;done
ffmpeg -r 30 -f concat -safe 0 -i list.txt -c:v libx264 -crf 18 -preset fast -c:a fast -c:a copy output-second.mp4
ffmpeg -i output-second.mp4 -i TEST4.mp3 -c:v copy -strict experimental -map 0:v:0 -map 1:a:0 TEST4-OUTPUT.mp4
