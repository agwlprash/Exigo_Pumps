# Introduction
Codes to use Cellix Exigo pumps using a Raspberry Pi or via Anaconda on a Windows PC

# Installing on Windows using Anaconda
```Python
conda install kivy -c conda-forge
pip install serial
```
Use the ExiGo-pump_v4.py for simple liquid dosing and withdrawal.
Please install the [USB drivers](USB drivers.zip) before running the code.

_To look at what does the 'ExiGo-pump_v4_COM5_test_PUMPCODE_glass_syringe.py' does_



# Installing on Raspberry pi

The depencies can be installed using the following [link](https://kivy.org/doc/stable/installation/installation-rpi.html)
The following code also installs Python 3.7 which is essential.

All these commands are present in the file name (Python_update)[Python_update.txt]

Save the following files: [ExiGo-pump_v4](ExiGo-pump_v4.py) and [Instructions_code](Instructions_code.txt), in _pi->home->My Documents_. If you are unfamiliar with Raspberry Pi then please follow the instructions in the file [Operating_instructions](Operating_instructions.txt)

```Python
sudo apt-get update
sudo apt-get upgrade
sudo apt update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
sudo tar zxf Python-3.7.0.tgz
cd Python-3.7.0
sudo ./configure
sudo make -j 4
sudo make altinstall

sudo ln -s /usr/local/opt/python-3.7.0/bin/pydoc3.7 /usr/bin/pydoc3.7
sudo ln -s /usr/local/opt/python-3.7.0/bin/python3.7 /usr/bin/python3.7
sudo ln -s /usr/local/opt/python-3.7.0/bin/python3.7m /usr/bin/python3.7m
sudo ln -s /usr/local/opt/python-3.7.0/bin/pyvenv-3.7 /usr/bin/pyvenv-3.7
sudo ln -s /usr/local/opt/python-3.7.0/bin/pip3.7 /usr/bin/pip3.7
alias python='/usr/bin/python3.7'
alias python3='/usr/bin/python3.7'
ls /usr/bin/python*
cd ..
sudo rm -r Python-3.7.0
rm Python-3.7.0.tar.xz
. ~/.bashrc

sudo apt update
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev
python -m pip install --upgrade --user pip setuptools
python -m pip install --upgrade --user Cython==0.29.10 pillow
python -m pip install --user kivy
```


## Fixing double click issues
There might be a problem with double key press in the API. For that, go to the explorer,and show hidden folders.   Then go to:  pi,  .config.ini and delete line 43,  starting with %(name)s
