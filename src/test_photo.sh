#!/bin/sh

raspistill -o ../temp_images/photo.jpg -w 1024 -h 768 -q 30
python email_sender.py

exit 0