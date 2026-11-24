#!/bin/bash
# final audio pass: -14 LUFS integrated (Instagram), -1 dBTP, AAC 256k; video stream copied untouched
set -e
ffmpeg -v error -y -i "$1" -c:v copy -af "loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000" -c:a aac -b:a 256k -movflags +faststart "$2"
