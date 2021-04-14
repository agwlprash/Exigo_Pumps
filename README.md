# Cellix-Pump-code-glass-syringe
This script allows the Cellix pump to be run by your computer without the Ipad that comes with it. The script includes some strings with serial code for the pump, change them only if you are sure of the changes (check the manual for the serial communications of the [pump](https://www.wearecellix.com/exigopump)). This script is set to run with a glass syringe.


# Installing on Raspberry pi

sudo apt-get update

sudo apt-get upgrade

sudo apt update

sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \

   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   
   python-setuptools libgstreamer1.0-dev git-core \
   
   gstreamer1.0-plugins-\{bad,base,good,ugly\} \
   
   gstreamer1.0-\{omx,alsa\} python-dev libmtdev-dev \
   
   xclip xsel libjpeg-dev
   
sudo pip install kivy

sudo pip install kivy-garden
