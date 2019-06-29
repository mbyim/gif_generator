#!/usr/bin/env bash
#Script takes args and creates a gif

#args needed:
#start time in hh:mm:ss
#$4
#time to grab (eg "grab two seconds")
#$5
#filename + path
#$1
#gifname?
#$3
#path to save/create
#$2
#patrol cycle flag
#$6

#cd "$1"
#echo "$PWD"
#00:08:04


#just run script w/o arg to get arg documentation
if [ $# -eq 0 ]
	then
	echo "Arguments:"
	echo "1: path_to_file"
	echo "2: path_to_save"
	echo "3: gif_name"
	echo "4: start_time-> 00:00:00"
	echo "5: length_to_grab"
	echo "6 [optional]: patrol_cycle_flag (leave blank to exclude step)"
	exit 0
fi


#added $3 to save path
ffmpeg -ss "$4" -t "$5" -i "$1" "$2/$3_frame_%03d.jpg"
#make into gif)
convert -delay 1x23 -loop 0 "$2" "$2"/*.jpg "$2"/"$3".gif

#resize - for now 30 (cahnge back to 30 later fuck twitter)
convert "$2"/"$3".gif -resize 15%  "$2"/quarter_"$3".gif

#make gif into patrol if needed
if [ $# -eq 6 ]
	then 
		convert "$2"/quarter_"$3".gif -coalesce -duplicate 1,-2-1 -quiet -layers OptimizePlus -loop 0  "$2"/patrol_"$3".gif
fi

#remove the actual frames themselves
echo "$2"
echo "$3"
rm "$2"/"$3"_frame_*.jpg

echo "completed and cleaned"
#/Downloads/Children of Men 2006 BluRay  1080p DTS x264-PRoDJi
