import serial
import time

import threading
import sys
import os
import argparse

import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog

from ctypes import c_uint32
from ctypes import c_uint16
import binascii  

import socket
import json


import random

import ctypes
from ctypes import *

#from PIL import Image









def sendFsData(serialPort):
		sendFileObj = open('fs_hex.ryfs', 'rb')
		
		sendFileData = sendFileObj.read()
		
		imageFileLen = len(sendFileData)
		
		imageDataHead = bytearray([0] * 12)
		imageDataHead[0] = 0x22
		imageDataHead[1] = 0xAA
		
		imageDataHead[4]  = (imageFileLen >>  0) & 0x000000ff;
		imageDataHead[5]  = (imageFileLen >>  8) & 0x000000ff;
		imageDataHead[6]  = (imageFileLen >> 16) & 0x000000ff;
		imageDataHead[7]  = (imageFileLen >> 24) & 0x000000ff;
		
		send_size = 0
		sendFileObj.seek(0)
		count = 0
		while send_size < imageFileLen:
			
			tempData = sendFileObj.read(256)
			imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
			imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
			send_size = send_size + len(tempData)
			print(imageDataHead+tempData)
			print(len(imageDataHead+tempData))
			serialPort.write((imageDataHead+tempData));
			'''
			if count ==0 :
				time.sleep(8)
			time.sleep(0.2)
			'''
			resp = serialPort.read(1)
			while 1:
				resp = serialPort.read(1)
				#print(len(resp))
				#print(len(resp))
				if len(resp) != 0:
					break
			#print(resp)
			time.sleep(0.02)
			
			print("imageFileLen = %d ,count = %d , sendSize = %d"%(imageFileLen, count, send_size))
			count = count + 1



def parse_arguments():

	parser = argparse.ArgumentParser()
	#parser.add_argument('--debug', dest='debug', default='0')
	#parser.add_argument('--port', dest='port', default='54324')
	#parser.add_argument('--IP', dest='IP', default='192.168.1.1')
	parser.add_argument('--serial', dest='serial', default='com22')
	parser.add_argument('--baudrate', dest='baudrate', default='115200')
	parser.add_argument('--path', dest='path', default='.\\data\\')
	
	args = parser.parse_args()
	
	return args

def sendResData(file_name, serialPort):
	print(file_name)
	sendFileObj = open(file_name, 'rb')
	
	sendFileData = sendFileObj.read()
	
	imageFileLen = len(sendFileData)
	#fileName = (self.offsetSelection.get())
	
			
	lowerName = file_name.lower()

		
	imageFileLen = len(sendFileData)
	
	
	imageDataHead = bytearray([0] * 12)
	imageDataHead[0] = 0x33
	imageDataHead[1] = 0xAA
	
	imageDataHead[4]  = (imageFileLen >>  0) & 0x000000ff;
	imageDataHead[5]  = (imageFileLen >>  8) & 0x000000ff;
	imageDataHead[6]  = (imageFileLen >> 16) & 0x000000ff;
	imageDataHead[7]  = (imageFileLen >> 24) & 0x000000ff;
	
	#imageDataHead[8]  = (offset >>  0) & 0x000000ff;
	#imageDataHead[9]  = (offset >>  8) & 0x000000ff;
	#imageDataHead[10]  = (offset >> 16) & 0x000000ff;
	#imageDataHead[11]  = (offset >> 24) & 0x000000ff;
	
	send_size = 0
	sendFileObj.seek(0)
	count = 0
	while send_size < imageFileLen:
		
		#tempData = sendFileObj.read(256)
		#imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
		#imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
		
		#send_size = send_size + len(tempData)
		#print(imageDataHead+tempData)
		#self.serialPort.write((imageDataHead+tempData));
		
		if count == 0 :
			#send_size = send_size + len(tempData)
			imageDataHead[2]  = (0 >>  0) & 0x000000ff;
			imageDataHead[3]  = (0 >>  8) & 0x000000ff;
			print((imageDataHead + bytes(file_name, encoding="utf8") ))
			serialPort.write((imageDataHead + bytes(file_name,encoding="utf8") ));
			time.sleep(5)
		else:
			tempData = sendFileObj.read(256)
			imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
			imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
			send_size = send_size + len(tempData)
			print(imageDataHead+tempData)
			serialPort.write((imageDataHead+tempData));
			
			time.sleep(0.3)
		print("imageFileLen = %d ,count = %d , sendSize = %d"%(imageFileLen, count, send_size))
		count = count + 1
		
	print("finish")
	
	pass


if __name__ == '__main__':

	args = parse_arguments()
	serialPort = serial.Serial(args.serial, int(args.baudrate), timeout=0)
	sendFsData(serialPort)
	
	'''
	file_list = os.listdir(args.path)
	print(file_list)
	for cur_file in file_list:
		sendResData(args.path + cur_file, serialPort)
	'''











