# Raspberry-Pi-Door-Entry

This door entry system makes use of a 433MHz-116dBm low-noise shielded receiver module AM Super Heterodyne (receiver range 30 metres+), Lloytron MIP wireless doorbell, Raspberry Pi 3 B and Raspberry Pi Camera Module. 

Credit to H M Bennett for providing many of the resources.

HOW TO USE:

run main.py to register and access database. There you can add details of people and photos of their faces which will be processed and encoded. Make sure you remember to click the encode button to encode new photos added.

If you look inside email_sender.py, you will see that I have used environment variables for my email info. You will need to edit the SENDER and PASS so you can send yourself or others emails.

PLEASE NOTE: If you do not have two-factor authentication on, you will need to go [here](https://myaccount.google.com/lesssecureapps) and turn on less secure apps for the sender email. If you do, you will need to go [here](https://myaccount.google.com/apppasswords) and generate a password. Make sure you remember it.

T