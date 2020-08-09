#!/bin/sh

raspistill -o photo.jpg -w 1024 -h 768 -q 30
python doorbell_press.py

exit 0