from time import sleep
#import usb.core
#from serial.tools import list_ports
import serial
import time
import os
from datetime import datetime, timedelta
from threading import Thread, Event

from kivy.app import App
#kivy.require("1.8.0")
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.lang import Builder
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#comList=list_ports.comports()
#print (comList)
global ser
st = 0
sta = 0
sta2 = 0

#ser = serial.Serial('/dev/ttyUSB0',baudrate=38400,bytesize=8,timeout=0.5)
init = b'\x1b I \x00' # initialize pump (home position)
stop = b'\x1b P \x00' # stop pump
syr = b'\x1b Q Y \x00' # query syringe type
setsyr = b'\x1b S Y 2 \x00' #set syringe type
flrt = b'\x1b S F 1000 \x00' #set flow rate in nl/min
c1 = b'\x1b S A 0 2 C 5000 0 20 \x00'
c2 = b'\x1b S A 1 2 R 0 3000 0 0 \x00'
c3 = b'\x1b S A 2 2 C 0 1 0 \x00'
drop = b'\x1b S A 0 1 C 150000 0 4 \x00'
drop2 = b'\x1b S A 1 1 C 0 0 1 \x00'
run = b'\x1b T \x00'
query = b'\x1b Q S \x00'

class main(GridLayout):
    def __init__(self, **kwargs):
        super(main, self).__init__(**kwargs)
        self.cols = 1
        self.row_force_default=True
        self.row_default_height=40
        #self.spacing = [10,0]
        self.add_widget(Label(text="Microfluidic Pump Control"))

        self.pump = GridLayout()
        self.pump.cols = 2
        self.pump.row_force_default=True
        self.pump.row_default_height=40
        #self.pump.spacing = [10,0]
        

        self.init = Button(text="Initialise Pump")
        self.add_widget(self.init)
        self.init.bind(on_press = self.initpump)
        self.prg = Button(text="Purge")
        self.add_widget(self.prg)
        self.str = Button(text="Start")
        self.add_widget(self.str)
        self.str.bind(on_press = self.start)
        self.stp = Button(text="Stop")
        self.add_widget(self.stp)
        self.stp.bind(on_press = self.stop)
        
        
        self.pump.add_widget(Label(text="Flow Rate (ul/sec)"))
        self.flr = TextInput(multiline=False,input_type= ("number"), input_filter = ("float"), text = "0")
        self.pump.add_widget(self.flr)
        self.flr.bind(text = self.volume)
        self.pump.add_widget(Label(text="Flow Time (sec)"))
        self.flt = TextInput(multiline=False,input_type= ("number"), input_filter = ("int"), text = "0")
        self.pump.add_widget(self.flt)
        self.flt.bind(text = self.volume)
        
        self.pump.add_widget(Label(text="Flow Rate (ul/sec)"))
        self.flr2 = TextInput(multiline=False,input_type= ("number"), input_filter = ("float"), text = "0")
        self.pump.add_widget(self.flr2)
        self.flr2.bind(text = self.volume)
        self.pump.add_widget(Label(text="Flow Time (sec)"))
        self.flt2 = TextInput(multiline=False,input_type= ("number"), input_filter = ("int"), text = "0")
        self.pump.add_widget(self.flt2)
        self.flt2.bind(text = self.volume)
        
        self.pump.add_widget(Label(text="Flow Rate (ul/sec)"))
        self.flr3 = TextInput(multiline=False,input_type= ("number"), input_filter = ("float"), text = "0")
        self.pump.add_widget(self.flr3)
        self.flr3.bind(text = self.volume)
        self.pump.add_widget(Label(text="Flow Time (sec)"))
        self.flt3 = TextInput(multiline=False,input_type= ("number"), input_filter = ("int"), text = "0")
        self.pump.add_widget(self.flt3)
        self.flt3.bind(text = self.volume)

        self.add_widget(self.pump)
        
        self.pump = GridLayout()
        self.pump.cols = 1
        self.row_force_default=True
        self.row_default_height=40
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text="Information"))
        self.tvol = Label(text=("Total Volume = 0nl"))
        self.add_widget(self.tvol)
        self.pinit = Label(text=("Pump Not Initialised"))
        self.add_widget(self.pinit)
        self.info = Label(text=(""))
        self.add_widget(self.info)
        
        

    def connect(self):
        global ser
        try:
            ser.inWaiting()
        except:
            #print("connecting")
            try:
                ser = serial.Serial('COM5',baudrate=38400,bytesize=8,timeout=0.5)
                self.info.text = ("Pump connected")
            except:            
                x=os.system("COM5")
                if x==0:
                    #print("Pump connected but cant communicate")
                    self.info.text = ("Pump connected but cant communicate")
                else:
                    self.info.text = ("Pump disconnected")
                    #print("Pump disconnected")


    def initpump(self, instance):
        global ser
        self.send(init)
        
        self.send(setsyr)
        
    def start(self, instance):
        try:
            t = Thread(target=self.startt, args=()).start()
        except (SystemExit):
            sys.exit()
        
    def startt(self):
        global ser
        #global sta
        #sta = 1
        self.str.disabled = True
        self.init.disabled = True
        self.prg.disabled = True
        sec = timedelta(seconds=int(self.flt.text))
        d = datetime(1,1,1) + sec
        dm = d.minute + (d.hour*60)
        ds = d.second
        l = str.encode(str(int(float(self.flr.text)*60*1000)))
        m = str.encode(str(dm))
        s = str.encode(str(ds))
        
        sec2 = timedelta(seconds=int(self.flt2.text))
        d2 = datetime(1,1,1) + sec2
        dm2 = d2.minute + (d2.hour*60)
        ds2 = d2.second
        l2 = str.encode(str(int(float(self.flr2.text)*60*1000)))
        m2 = str.encode(str(dm2))
        s2 = str.encode(str(ds2))
        
        sec3 = timedelta(seconds=int(self.flt3.text))
        d3 = datetime(1,1,1) + sec3
        dm3 = d3.minute + (d3.hour*60)
        ds3 = d3.second
        l3 = str.encode(str(int(float(self.flr3.text)*60*1000)))
        m3 = str.encode(str(dm3))
        s3 = str.encode(str(ds3))
        #print(dm)
        #print(ds)
        d = b'\x1b S A 0 1 C ' + l + b' ' + m + b' ' + s + b' \x00'
        d2 = b'\x1b S A 0 1 C ' + l2 + b' ' + m2 + b' ' + s2 + b' \x00'
        d3 = b'\x1b S A 0 1 C ' + l3 + b' ' + m3 + b' ' + s3 + b' \x00'
        #print(d)
        #print(drop)
        self.send(d)
    
        self.send(drop2)

        self.send(run)
        sleep(int(self.flt.text) + 5)
        
        self.send(d2)
    
        self.send(drop2)

        self.send(run)
        sleep(int(self.flt2.text) + 5)
        
        self.send(d3)
    
        self.send(drop2)

        self.send(run)
        
        #check for assy still runing to re enable start button
        #self.str.disabled = False
##        while(sta):
##            q = self.send(query)
##            if(q == "?"):
##                break:
        #print("query")
        #print(self.send(query))
        self.str.disabled = False
        self.init.disabled = False
        self.prg.disabled = False

    def stop(self, instance):
        global ser
        global sta
        sta = 0
        self.send(b'\x1b P \x00')
        #print(self.send(query))

    def send(self, data):
        global ser
        self.connect()
        ser.write(data)
        sleep(1)
        #return(ser.readline())
        print(ser.readline())

    def volume(self, instance, value):
        try:
            l = float(self.flr.text)
        except:
            l = 0
        try:
            s = float(self.flt.text)
        except:
            s = 0
        vol = s*l
        self.tvol.text = ("Total Volume = " + str(vol) + "ul")
        

class pump(App):
    def build(self):
        return main()

if __name__ == "__main__":
    Config.set('graphics', 'width', 300)
    Config.set('graphics', 'height', 500)
    pump().run()
