#!/bin/sh

while true; do
    valid="(device code)"
    scan=`./433Utils/RPi_utils/RFSniffer.cpp`
    if [ "$scan" = "$valid" ]; then
        raspistill -o ../temp_images/photo.jpg -w 1024 -h 768 -q 30
        python handle_image.py
        t=`date +%T`
        d=`date +%d%m%y`
        echo "Doorbell pressed $t $d"
        echo "Doorbell pressed $t" >> ../log/log$d.txt
    else
        echo "Bad read. Code is $scan"
    fi
    sleep 20
done
exit 0 