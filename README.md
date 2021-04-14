# Introduction
Codes to use Cellix Exigo pumps using a Raspberry Pi or via Anaconda on a Windows PC

# Installing on Windows using Anaconda
```Python
conda install kivy -c conda-forge
pip install serial
```


# Installing on Raspberry pi

The depencies can be installed using the following [link](https://kivy.org/doc/stable/installation/installation-rpi.html)

```Python
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
```




# Fixing double click issues
There might be a problem with double key press in the API. For that, go to the explorer,and show hidden folders.   Then go to:  pi,  .config.ini and delete line 43,  starting with %(name)s
