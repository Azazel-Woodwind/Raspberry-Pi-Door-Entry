# Raspberry-Pi-Door-Entry

*This door entry system makes use of a 433MHz-116dBm low-noise shielded receiver module AM Super Heterodyne (receiver range 30 metres+), Lloytron MIP wireless doorbell, Raspberry Pi 3 B and Raspberry Pi Camera Module, however the functionality can be tested using only a linux or MacOS desktop or Raspberry Pi. Credit to H M Bennett for providing many of the resources.*

## SETUP (Read all before starting):

- This setup requires a Linux based or Mac OS, as some required functions are not supported or easily available on Windows.
- Please refer to the HOW TO USE section at the bottom of the page for how to attach the receiver module

###### Installation:
- Run these commands in the terminal to install and make all bash shells executable:
  ```bash
  $ git clone https://github.com/Azazel-Woodwind/Raspberry-Pi-Door-Entry.git
  $ cd Raspberry-Pi-Door-Entry/
  $ chmod a+x src/*.sh && chmod a+x src/433Utils/RPi_Utils/*.sh
  ```
- **PLEASE NOTE: WHEN RUNNING SCRIPTS, YOUR CURRENT WORKING DIRECTORY MUST BE THE SAME AS THE DIRECTORY OF THE SCRIPT OR IT WILL NOT WORK i.e cd into the directory before running anything**

###### OpenCV install:

 - Follow the instructions [here](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/) to install OpenCV for your OS. 
 - We will be using the OpenCV library to load, process and draw on images. I strongly recommend installing from source, as I ran into bugs when I tried to pip install.

###### Dlib install:

 - Follow the instructions [here](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/) to install dlib for your OS. 

- We will be indirectly using dlib as our method of face recognition.

  - ALTERNATIVELY, if you have an NVIDIA graphics card (which supports CUDA) and would like to test the functionality on your desktop, compile dlib from source with the following commands:

    ```bash
    $ git clone https://github.com/davisking/dlib.git
    $ cd dlib
    $ mkdir build
    $ cd build
    $ cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
    $ cmake --build .
    $ cd ..
    $ python setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA
    ```

###### Face_recognition install:

 - To install the face_recognition module, simply `pip install face_recognition` 
 - This module wraps around the dlib module and makes it much easier to use.
 - If you have an NVIDIA GPU and compiled dlib from source, navigate to line 17 in `src/recognise_face.py` and change the word "hog" to "cnn".

 ###### WiringPi install (Raspberry Pi 4 Only)
  - WiringPi comes installed by default on most most raspian systems, but if you are on the Raspberry Pi 4, issue the following commands:
    ```bash
    cd /tmp
    wget https://project-downloads.drogon.net/wiringpi-latest.deb
    sudo dpkg -i wiringpi-latest.deb
    ```
  - Navigate back to the project directory after this

###### Tkinter install:

 - If you are on Linux, tkinter may not be installed by default. To install, run `sudo apt install python-tk` in the terminal and restart your system.
 - Tkinter is the primary GUI library used to tamper with the database.

###### Pillow install:

 - If Pillow is not installed, run `pip install Pillow`.
 - Pillow is a popular module that we use to load images.

###### Configuring emails:

 - For emails to be sent, the smtp protocol must be able to log into an email account. 
 - You will see in `src/email_sender.py` that I have logged in using my email details that I have saved in my environment variables. If you want to receive emails, you will need to swap these details for your own, or any other email from which you would like to receive emails about photos taken.

**PLEASE NOTE: If you do not have two-factor authentication on, you will need to go [here](https://myaccount.google.com/lesssecureapps) and turn on less secure apps for the sender email. If you do, you will need to go [here](https://myaccount.google.com/apppasswords) and generate a password. Make sure you remember it.**


## HOW TO USE:

To recognise a face, the software must have a repository of known faces to compare with. To create this, run `src/main.py` which gives you access to an sqlite database that stores and retrieves photos and details of people you know. From there, you must add records of people you want to recognise, add photos to their records and then encode the data. 

**MAKE SURE that you encode every time you make a change, or the changes will not take effect.**

1. If you would like to test the functionality on a desktop without a raspberry pi, copy the image you would like to analyse into temp_images and rename it "photo.jpg". Then run `src/email_sender.py`. Provided you have correctly followed all the steps and have registered your email on the database, you should receive an email about the photo.

2. If you would like to test the functionality with a picture taken from a pi without an Lloytron input device (which I recommend you do first to test the camera), follow all the above steps for your raspberry pi, connect the camera module and run `src/test_photo.sh`. **If this errors, replace `python` with `python3` if you aren't running a virtual environment, however I recommend that you use one.**

3. If you would like to fully test the device using your raspberry pi, camera module, receiver and doorbell, please connect the receiver as shown below.

![Pi diagram](http://fav.me/de34x9d)

The red wire connects to 5 volt + on the Pi, the black wire connects to GND & the yellow wire
connects to GPIO 27 (which in WiringPi-speak is confusingly referred to as GPIO 2)
The blue wire in the picture is an optional antenna wire, which should be 17.3cm long & can be
coiled around a biro so it takes up less space. It is optional and generally not needed unless large distance transmissions are required.

- Then, navigate to 433Utils/RPi_utils and run `./test.sh`. Activate your doorbell and take note of the code.
- Navigate to shell_scripts/receiver.sh and change "(device code)" to the code you took note of.
- You're ready to go! Position your Raspberry Pi as suitable and run `src/receiver.sh` in the background. **If this errors, replace `python` with `python3` if you aren't running a virtual environment, however I recommend that you use one.** Then press your doorbell whenever you're ready, have your email open and watch the magic happen!

