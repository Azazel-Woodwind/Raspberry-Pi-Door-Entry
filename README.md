# Raspberry-Pi-Door-Entry

*This door entry system makes use of a 433MHz-116dBm low-noise shielded receiver module AM Super Heterodyne (receiver range 30 metres+), Lloytron MIP wireless doorbell, Raspberry Pi 3 B and Raspberry Pi Camera Module, however the functionality can be tested using only a linux or MacOS desktop or Raspberry Pi. Credit to H M Bennett for providing many of the resources.*

## SETUP:

- This setup requires a Linux based or Mac OS, as some required functions are not supported or easily available on Windows.

###### OpenCV install:

 - Follow the instructions [here](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/) to install OpenCV for your OS. 
 - We will be using the OpenCV library to load, process and draw on images. I strongly recommend installing from source, as I ran into bugs when I tried to pip install.

###### Dlib install:

 - Follow the instructions [here](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/v) to install dlib for your OS. 

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
 - If you have an NVIDIA GPU and compiled dlib from source, navigate to line 17 in `recognise_faces.py` and change the word "hog" to "cnn".

###### Tkinter install:

 - If you are on Linux, tkinter may not be installed by default. To install, run `sudo apt install python-tk` in the terminal and restart your system.
 - Tkinter is the primary GUI library used to tamper with the database.

###### Pillow install:

 - If Pillow is not installed, run pip install Pillow.
 - Pillow is a popular module that we use to load images.

###### Configuring emails:

 - For emails to be sent, the smtp protocol must be able to log into an email account. 
 - You will see in `email_sender.py` that I have logged in using my email details that I have saved in my environment variables. If you want to receive emails, you will need to swap these details for your own, or any other email from which you would like to receive emails about photos taken.

**PLEASE NOTE: If you do not have two-factor authentication on, you will need to go [here](https://myaccount.google.com/lesssecureapps) and turn on less secure apps for the sender email. If you do, you will need to go [here](https://myaccount.google.com/apppasswords) and generate a password. Make sure you remember it.**


## HOW TO USE:

To recognise a face, the software must have a repository of known faces to compare with. To create this, run `main.py` which gives you access to an sqlite database that stores and retrieves photos and details of people you know. From there, you must add records of people you want to recognise, add photos to their records and then encode the data. 

**MAKE SURE that you encode every time you make a change, or the changes will not matter.**

1. If you would like to test the functionality on a desktop without a raspberry pi, copy the image you would like to analyse into the same directory as the source code and rename it "photo.jpg". Then run `process.py`. Provided you have correctly followed all the steps and have registered your email on the database, you should receive an email about the photo.

2. If you would like to test the functionality with a picture taken from a pi without an Lloytron input device, follow all the above steps for your raspberry pi, connect the camera module and run `test1.sh`. **If this errors, replace `python` with `python3` if you aren't running a virtual environment, however I recommend that you use one.**

3. Instructions for the Lloytron devices are coming soon.

