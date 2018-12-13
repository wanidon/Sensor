#!/usr/bin/env python2
#coding:utf-8
import time
import picamera
import commands
#from PIL import Image, ImageOps
#import ToBin

def cameraTest():
        with  picamera.PiCamera() as cam:
                cam.resolution = (400,300)
                cam.start_preview()
                time.sleep(8)
                cam.capture("testimage.jpg")

if __name__ == "__main__":
    while True:
        cameraTest()

        
