#!/bin/sh

python email_sender.py
t=`date +%T`
d=`date +%d%m%y`
echo "Doorbell pressed $t $d"
echo "Doorbell pressed $t" >> ../log/log$d.txt

exit 0