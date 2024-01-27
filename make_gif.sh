#!/bin/bash
s=""
for ((n=0;n<=198;n++))
do
	s="${s} gif_frame${n}.png"
done

convert -delay 10 -loop 0  ${s} km.gif

