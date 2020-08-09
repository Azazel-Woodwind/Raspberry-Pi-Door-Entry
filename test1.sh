#!/bin/sh

raspistill -o photo.jpg -w 1024 -h 768 -q 30
python process.py

exit 0