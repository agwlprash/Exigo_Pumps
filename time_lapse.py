import RPi.GPIO as GPIO
from pyueye import ueye
import numpy as np
import cv2
import sys
import time
import matplotlib.pyplot as plt
import math
#import LDR_mods as funcs
import os


imfoldname='time_lapse_test'
filename='300_XG1500_ERH70'
sleeptime=300 #in seconds


#######################################################
##########Camera properties############################


if os.path.isdir(imfoldname):
    print('Directory exists')
else:
    os.mkdir(imfoldname)

#today=time.localtime(time.time())
#date=str(today.tm_year)+'-'+str(today.tm_mon)+'-'+str(today.tm_mday)

#Camera AOI properties
x=0
y=0
width=800
height=600




framerate=10	#frame rate
exposure=1

print('Camera AOI:  (x,y,width,height) = (%d,%d,%d,%d)' % (x,y,width,height))

hCam = ueye.HIDS(0) #0: first available camera;  1-254: camera ID
sInfo = ueye.SENSORINFO()
cInfo = ueye.CAMINFO()
pcImageMemory = ueye.c_mem_p()
MemID = ueye.int()

rect_AOI = ueye.IS_RECT()

rect_AOI.s32X = ueye.INT(x)
rect_AOI.s32Y = ueye.INT(y)
rect_AOI.s32Width = ueye.INT(width)
rect_AOI.s32Height = ueye.INT(height)

   
pitch = ueye.INT()
nBitsPerPixel = ueye.INT(8)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
channels = 1                    #3: channels for color mode(RGB); take 1 channel for monochrome
m_nColorMode = ueye.INT()       # Y8/RGB16/RGB24/REG32
bytes_per_pixel = int(nBitsPerPixel / 8)
#---------------------------------------------------------------------------------------------------------------------------------------
print "START" 

# Starts the driver and establishes the connection to the camera
nRet = ueye.is_InitCamera(hCam, None)
if nRet != ueye.IS_SUCCESS:
    print("is_InitCamera ERROR")
# Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
nRet = ueye.is_GetCameraInfo(hCam, cInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetCameraInfo ERROR")
# You can query additional information about the sensor type used in the camera
nRet = ueye.is_GetSensorInfo(hCam, sInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetSensorInfo ERROR")

nRet = ueye.is_ResetToDefault( hCam)
if nRet != ueye.IS_SUCCESS:
    print("is_ResetToDefault ERROR")

# Set display mode to DIB
nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)
def from_bytes (data, big_endian = False):
    if isinstance(data, str):
        data = bytearray(data)
    if big_endian:
        data = reversed(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    return num
## Set the right color mode
if from_bytes(sInfo.nColorMode.value) == ueye.IS_COLORMODE_BAYER:
    # setup the color depth to the current windows setting
    ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
    bytes_per_pixel = int(nBitsPerPixel / 8)
elif from_bytes(sInfo.nColorMode.value) == ueye.IS_COLORMODE_CBYCRY:   
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_BGRA8_PACKED
    nBitsPerPixel = ueye.INT(32)
    bytes_per_pixel = int(nBitsPerPixel / 8)
elif from_bytes(sInfo.nColorMode.value) == ueye.IS_COLORMODE_MONOCHROME:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
else:
    # for monochrome camera models use Y8 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)

width = rect_AOI.s32Width
height = rect_AOI.s32Height

nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_SET_AOI, rect_AOI, ueye.sizeof(rect_AOI))
if nRet != ueye.IS_SUCCESS:
    print "is_AOI ERROR"


# Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
if nRet != ueye.IS_SUCCESS:
    print("is_AllocImageMem ERROR")
else:
    # Makes the specified image memory the active memory
    nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetImageMem ERROR")
    else:
        # Set the desired color mode
        nRet = ueye.is_SetColorMode(hCam, m_nColorMode)
# Activates the camera's live video mode (free run mode)
nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
if nRet != ueye.IS_SUCCESS:
    print("is_CaptureVideo ERROR")
# Enables the queue mode for existing image memory sequences
nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
if nRet != ueye.IS_SUCCESS:
    print("is_InquireImageMem ERROR")
else:
    print("Press Ctrl+C to leave the program")


starttime=time.time()
imgct=0

oldtime=0

try:
    # Main loop
    while True:
        imgct+= 1
        timenow=time.time()
        tdiff=timenow-starttime
        
        timediffomega=tdiff-oldtime
        
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)
        frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
        
        cvfilename = imfoldname+'/'+filename+"_00" +  str(int(timenow)) + ".jpg"
        cv2.imwrite(cvfilename, frame)
        cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)
        
        time.sleep(sleeptime)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    log.close()
    # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
    ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)
    # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
    ueye.is_ExitCamera(hCam)
    # Destroys the OpenCv windows
    cv2.destroyAllWindows()
    print "END"





