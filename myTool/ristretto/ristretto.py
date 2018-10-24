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

from PIL import Image

from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRC32 import CRC32
from PyCRC.CRCCCITT import CRCCCITT

'''
#服务端
sk = socket.socket()

sk.bind(("127.0.0.1", 8888))

sk.listen(2)
#conn,addr = sk.accept()


#recv_data = conn.recv(1024)
#conn.sendall(bytes("test string", encoding="utf8"))

def socket_thread():
	conn,addr = sk.accept()
'''	
#serialPort = serial.Serial('com8',115200,timeout=1)

'''
#客户端
sk = socket.socket()

sk.connect(("127.0.0.1", 8888))


'''
 
ll = ctypes.cdll.LoadLibrary
'''
lib = ll("./libloader_win64.so")
file = c_char_p(b'test3')
#lib.inputJsonFile.argtypes = [c_char_p]
lib.inputJsonFile( file)
'''





		



def checkIsDigit(content):
	if content.isdigit() or (content==''):
		return True
	else:
		return False


class Application():
	def __init__(self, master=None, debug=1):
		self.frame = Tk()
		self.frame.geometry('500x300')
		self.filename = ''
		self.filenameVar = StringVar()
		self.maxPackSize = 240*1024
		
		self.checkInput = self.frame.register(checkIsDigit)
				
		self.createWidgets()
		self.debug = 1
		
		self.testFunctionFlag = 0
		self.frame1 = Frame(self.frame)
		self.widgetNameDict = {'NONE':0, 'UI':100, 'OTA':200, 'module':300,'Font':301,'Resource':302,'fs':303, 'Touch':400, "NFC":401, 'Gsensor':402, 'HRM': 403,'Motar':404,'Led':405,'Power Manage':406 }
		self.jsonDict = {"test1":"test string1","test2":"test string2","test3":"test string3","test4":"test string5",}
		
	def clearPara(self):
		self.filename = ''
		self.filenameVar.set(self.filename);
		
		
		
		
	def getRandomID(self):
		
		randomStart = self.testFunctionFlag *100
		randomEnd = randomStart + 99
		
		return random.randint(randomStart, randomEnd)
		
	def checkWidgetChanged(self,widgetName):
		
		if self.testFunctionFlag == self.widgetNameDict[widgetName]:
			return False
		else:
			if self.testFunctionFlag != 0:
				self.frame1.destroy()
				self.frame1 = Frame(self.frame)
			
			self.testFunctionFlag = self.widgetNameDict[widgetName]
			
			self.frame.title('ryeex test ---' + widgetName)
			
			self.clearPara()
			if self.debug == 1:
				print('current widget is %s'%(widgetName))
				
			return True
			
	def jsonDataTransfer(self,jsonData):
		#print(self.debug)
		if self.debug == 1:
			print((jsonData))
		elif self.debug ==0:
			sk.sendall(bytes(jsonData))
			
		elif self.debug == 2:
			print(bytes(jsonData, encoding="utf8"))
			self.serialPort.write(bytes(jsonData, encoding="utf8"));
			
		self.waitJsonResponse()
			
	def waitJsonResponse(self):
		if self.debug == 1:
			return
		elif self.debug ==0:
			json_str = str(sk.recv(2048) , encoding='utf8')
			
		elif self.debug == 2:
			json_str = self.serialPort.read(2048);
			
		#print(json_str)
		dict_test = json.loads(json_str)
		
		print(dict_test)
			
		#错误则跳出
		if 'error' in dict_test:
			print('error')
			messagebox.showerror('error', dict_test['error']['message'])
			return
		

	def createWidgets(self):
		
		
		self.MenuTest = Menu(self.frame, tearoff = 1)
		self.MenuTest.add_command(label='UI', command=self.uiTestFrameCreate)
		#self.MenuTest.add_command(label='Device', command=self.deviceTestFrameCreate)
		#self.MenuTest.add_command(label='module', command=self.moduleTestFrameCreate)
		self.MenuTest.add_command(label='OTA', command= self.otaTestFrameCreate)
		
		self.MenuModule = Menu(self.MenuTest,tearoff = 0)
		self.MenuModule.add_command(label='font', command = self.sendFontFileFrameCreate)
		self.MenuModule.add_command(label='Resource', command = self.sendResourceFrameCreate)
		self.MenuModule.add_command(label='FileSystem', command = self.sendFsFrameCreate)
		self.MenuModule.add_command(label='module4')
		
		self.MenuDevice = Menu(self.MenuTest,tearoff = 0)
		self.MenuDevice.add_command(label='Touch', command=self.touchTestFrameCreate)
		self.MenuDevice.add_command(label='NFC', command = self.nfcTestFrameCreate)
		self.MenuDevice.add_command(label='Gsensor')
		self.MenuDevice.add_command(label='HRM')
		self.MenuDevice.add_command(label='Motar', command = self.motarTestFrameCreate)
		self.MenuDevice.add_command(label='Led', command = self.ledTestFrameCreate)
		self.MenuDevice.add_command(label='Power Manage', command = self.PmTestFrameCreate)
		
		self.MenuTest.add_cascade(label='module', menu = self.MenuModule)
		self.MenuTest.add_cascade(label='Device', menu = self.MenuDevice)
		
		#self.MenuTest.add_command(label='module')
		self.frame.config(menu=self.MenuTest)
		
		#self.MenuTest.pack()
		
	def configFrameCreate(self):
		
		pass
		
		
	def uiTestFrameCreate(self):
		
		if self.checkWidgetChanged('UI') == False:
			return
		

			
		#if self.testFunctionFlag != 0:
			#self.frame1.destroy()
		
		#self.frame1 = Frame(self.frame)
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile, width = 20)
		self.openFileButton.grid(row=0, column=0)#pack(side=LEFT)
		
		self.sendButton = Button(self.frame1, text='send data', command=self.sendData, width = 20)
		self.sendButton.grid(row=0, column=1)#pack(side=RIGHT)
		
		self.refreshButton = Button(self.frame1, text='refresh', command=self.uiRefreshPicture, width = 20)
		self.refreshButton.grid(row=0, column=2)#pack(side=RIGHT)
		
		Label(self.frame1,text = 'File : ', width = 20, anchor = 'e').grid(row=1, column=0)
		self.uiFileDisplayLabel =  Label(self.frame1,textvariable = self.filenameVar, width = 20, anchor = 'e')
		self.uiFileDisplayLabel.grid(row=1, column=1)
		
		self.brightScale = Scale(self.frame1,from_=0, to=100,orient=HORIZONTAL)
		self.brightScale.grid(row=2,column = 0) 
		self.brightnessButton = Button(self.frame1, text='brightness', command=self.uiBrightness, width = 20)
		self.brightnessButton.grid(row=3, column=0)#pack(side=RIGHT)
		
		self.resizeScale = Scale(self.frame1,from_=0, to=100,orient=HORIZONTAL)
		self.resizeScale.grid(row=2,column = 1) 
		self.resizeButton = Button(self.frame1, text='resize', command=self.uiResizePicture, width = 20)
		self.resizeButton.grid(row=3, column=1)#pack(side=RIGHT)
		
		Label(self.frame1,text = "width", width = 20, anchor = 'e').grid(row=4, column=0)
		Label(self.frame1,text = "length", width = 20, anchor = 'e').grid(row=5, column=0)
		Label(self.frame1,text = "sx", width = 20, anchor = 'e').grid(row=6, column=0)
		Label(self.frame1,text = "sy", width = 20, anchor = 'e').grid(row=7, column=0)
		#width
		self.widthString = StringVar()
		self.widthString.set('0')#输入的绑定值
		self.widthSelection = ttk.Entry(self.frame1,textvariable = self.widthString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.widthSelection.grid(row=4, column=1)
		#length
		self.lengthString = StringVar()
		self.lengthString.set('0')#输入的绑定值
		self.lengthSelection = ttk.Entry(self.frame1,textvariable = self.lengthString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.lengthSelection.grid(row=5, column=1)
		#sx
		self.sxString = StringVar()
		self.sxString.set('0')#输入的绑定值
		self.sxSelection = ttk.Entry(self.frame1,textvariable = self.sxString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.sxSelection.grid(row=6, column=1)
		#sy
		self.syString = StringVar()
		self.syString.set('0')#输入的绑定值
		self.sySelection = ttk.Entry(self.frame1,textvariable = self.syString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.sySelection.grid(row=7, column=1)
		
		
		self.frame1.grid(row=2, column=2)
		#print('uiTestFrameCreate')
		pass
		
		
	def deviceTestFrameCreate(self):
	
		if self.checkWidgetChanged('Device') == False:
			return
		
		#if self.testFunctionFlag != 0:
			#self.frame1.destroy()
		
		
		#self.frame1 = Frame(self.frame)
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.pack(side=LEFT)
		self.frame1.pack(side = TOP)
		
	def moduleTestFrameCreate(self):
		
		if self.checkWidgetChanged('module') == False:
			return
		
		#if self.testFunctionFlag != 0:
			#self.frame1.destroy()
		
		#self.frame1 = Frame(self.frame)
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.grid(row = 0)
		self.frame1.pack(side = LEFT)
		
		
	def otaTestFrameCreate(self):
		if self.checkWidgetChanged('OTA') == False:
			return
		
		#if self.testFunctionFlag != 0:
			#self.frame1.destroy()
		
		#self.frame1 = Frame(self.frame)
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.grid(row = 0)
		self.frame1.pack(side = RIGHT)
		
	def sendFontFileFrameCreate(self):
		if self.checkWidgetChanged('Font') == False:
			return
			
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.grid(row = 0)
		
		
		self.sendButton = Button(self.frame1, text='send data', command=self.sendTTFData, width = 20)
		self.sendButton.grid(row=0, column=1)#pack(side=RIGHT)
		
		self.frame1.pack()
		
	def sendFsFrameCreate(self):
		if self.checkWidgetChanged('fs') == False:
			return
			
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.grid(row = 0)
		
		
		self.sendButton = Button(self.frame1, text='send data', command=self.sendFsData, width = 20)
		self.sendButton.grid(row=0, column=1)#pack(side=RIGHT)
		
		'''
		Label(self.frame1,text = 'file name').grid(row = 1,column = 0)
		
		
		self.offsetString = StringVar()
		self.offsetString.set('0')#输入的绑定值
		self.offsetSelection = ttk.Entry(self.frame1,textvariable = self.offsetString)
		self.offsetSelection.grid(row=1, column=1)
		'''
		self.frame1.pack()
		
	def sendFsData(self):
		sendFileObj = open(self.filename, 'rb')
		
		sendFileData = sendFileObj.read()
		
		imageFileLen = len(sendFileData)
		print(int(CRCCCITT().calculate(sendFileData) ) )
		
		if self.debug == 2:
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
				
				if count == 0:
					self.serialPort.write((imageDataHead))
					while  len(self.serialPort.read(1)) == 0:
						print("wait start")
					count = 1
					continue
					
				tempData = sendFileObj.read(256)
				imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
				imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
				
				imageDataHead[8]  = (count >>  0) & 0x000000ff;
				imageDataHead[9]  = (count >>  8) & 0x000000ff;
				imageDataHead[10]  = (count >> 16) & 0x000000ff;
				imageDataHead[11]  = (count >> 24) & 0x000000ff;
				
				send_size = send_size + len(tempData)
				print(imageDataHead+tempData)
				self.serialPort.write((imageDataHead+tempData));
				
				temp_crc = int((CRCCCITT().calculate(bytes(imageDataHead+tempData)) ))
				pack_crc = (temp_crc)
				#read_str = self.serialPort.read(2)
				print(pack_crc)
				'''
				while  len(read_str) == 0:
					read_str = self.serialPort.read(2)
					print("wait ACK")
					self.serialPort.write((imageDataHead+tempData));
				'''
				while 1 :
					print("wait read")
					read_str = self.serialPort.read(2)
					if len(read_str) == 0 :
						time.sleep(0.1)
						self.serialPort.write((imageDataHead+tempData));
						continue
					if (int.from_bytes(read_str, byteorder = 'little')) != pack_crc:
						print("p crc = 0x%x"%(temp_crc))
						print("wait ACK,%d\t-crc=0x%x"%(count,(int.from_bytes(read_str, byteorder = 'little'))))
						return
						self.serialPort.write((imageDataHead+tempData));
					else:
						print("CRC OK %d--%x--%x"%(count,pack_crc,(int.from_bytes(read_str, byteorder = 'little'))))
						break
				'''
				else:
					while 1:
						if (int.from_bytes(read_str, byteorder = 'little')) != pack_crc:
							print("p crc = 0x%x"%(temp_crc))
							print("wait ACK,%d\t-crc=0x%x"%(count,(int.from_bytes(read_str, byteorder = 'little'))))
							self.serialPort.write((imageDataHead+tempData));
						else:
							print("CRC OK %d--%x"%(count,(int.from_bytes(read_str, byteorder = 'little'))))
							break
				'''
				print((int.from_bytes(read_str, byteorder = 'little')))
				
				
				time.sleep(0.1)
				
				print("imageFileLen = %d ,count = %d , sendSize = %d"%(imageFileLen, count, send_size))
				count = count + 1
		
		
		
	def sendResourceFrameCreate(self):
		if self.checkWidgetChanged('Resource') == False:
			return
			
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.grid(row = 0)
		
		
		self.sendButton = Button(self.frame1, text='send data', command=self.sendResData, width = 20)
		self.sendButton.grid(row=0, column=1)#pack(side=RIGHT)
		
		Label(self.frame1,text = 'file name').grid(row = 1,column = 0)
		
		
		self.offsetString = StringVar()
		self.offsetString.set('0')#输入的绑定值
		self.offsetSelection = ttk.Entry(self.frame1,textvariable = self.offsetString)
		self.offsetSelection.grid(row=1, column=1)
		
		self.frame1.pack()
		
	def sendResData(self):
		sendFileObj = open(self.filename, 'rb')
		
		sendFileData = sendFileObj.read()
		
		imageFileLen = len(sendFileData)
		fileName = (self.offsetSelection.get())
		
		
		if self.debug == 2:
			
			lowerName = self.filename.lower()
			if os.path.splitext(lowerName)[1] == '.png':
				#转换为bmp文件
				im = Image.open(self.filename)
				im = im.convert("RGB")
				#im = im.transpose(Image.FLIP_LEFT_RIGHT)
				im = im.transpose(Image.FLIP_TOP_BOTTOM)
				im.save(lowerName + '.bmp','bmp')
				
				sendFileObj = open(lowerName + '.bmp', 'rb')
		
				sendFileData = sendFileObj.read();
				
				print('covert to bmp')
				
			imageFileLen = len(sendFileData)
			
			temp_test = sendFileData[0:4095]
			input = b'\x01\x02\x03'
			print(int(CRCCCITT().calculate(input) ) )
			print(int(CRCCCITT().calculate(temp_test) ) )
			print(int(CRCCCITT().calculate(sendFileData) ) )
			
			
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
					print((imageDataHead + bytes(fileName, encoding="utf8") ))
					self.serialPort.write((imageDataHead + bytes(fileName,encoding="utf8") ));
					time.sleep(5)
				else:
					tempData = sendFileObj.read(256)
					imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
					imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
					send_size = send_size + len(tempData)
					print(imageDataHead+tempData)
					self.serialPort.write((imageDataHead+tempData));
					
					#time.sleep(0.5)
					read_str = self.serialPort.read(1)
					while  len(read_str) == 0:
						read_str = self.serialPort.read(1)
						print("wait ACK")
						self.serialPort.write((imageDataHead+tempData));
					print(read_str)
					time.sleep(0.05)
						
				print("imageFileLen = %d ,count = %d , sendSize = %d"%(imageFileLen, count, send_size))
				count = count + 1
				
				'''
				read_str = self.serialPort.read(2048)
				while  len(read_str) == 0:
					read_str = self.serialPort.read(2048)
					print("wait ACK")
				'''
					
				
				
			print("finish")
		
		pass
		
		
	def sendTTFData(self):
		sendFileObj = open(self.filename, 'rb')
		
		sendFileData = sendFileObj.read()
		
		imageFileLen = len(sendFileData)
		
		if self.debug == 2:
			imageDataHead = bytearray([0] * 8)
			imageDataHead[0] = 0x44
			imageDataHead[1] = 0xAA
			
			imageDataHead[4]  = (imageFileLen >>  0) & 0x000000ff;
			imageDataHead[5]  = (imageFileLen >>  8) & 0x000000ff;
			imageDataHead[6]  = (imageFileLen >> 16) & 0x000000ff;
			imageDataHead[7]  = (imageFileLen >> 24) & 0x000000ff;
			
			send_size = 0
			sendFileObj.seek(0)
			while send_size < imageFileLen:
				
				tempData = sendFileObj.read(256)
				imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
				imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
				send_size = send_size + len(tempData)
				print(imageDataHead+tempData)
				self.serialPort.write((imageDataHead+tempData));
				time.sleep(0.02)
				print("sleep")
		

	def openFile(self):
		self.filename = tkinter.filedialog.askopenfilename(title='打开文件',filetypes=[('All Files', '*')])
		self.filenameVar.set(self.filename);
		
	def sendData(self):
		sendFileObj = open(self.filename, 'rb')
		
		sendFileData = sendFileObj.read();
		
		#print(sendFileData.strip('\n'))
		#print(sendFileData)
		#print((sendFileData.replace('\n','').encode('UTF-8')) )
		#print(unicode('你好'))
		
		#self.jsonDict["bitmap"] = sendFileData
		
		#转为list发送数据
		#bmpListData = list(sendFileData)
		#self.jsonDict["bitmap"] = bmpListData
		
		'''
		bmpListData = list(sendFileData)
		print(bmpListData)
		test111 = str(bytearray(bmpListData))
		print(test111)
		bmpHexStringData = binascii.b2a_hex( test111 )
		self.jsonDict["bitmap"] = bmpHexStringData
		
		json_str = json.dumps(self.jsonDict)
		temp_str = str(json_str)
		print(len(temp_str))
		#print(bytes(json_str, encoding="utf8"))
		#print((json_str))
		#sk.sendall(bytes(json_str))
		'''
		
		#发送开始的json命令
		
		dict_test = {"id":123, "method":"img_add", "para":{"width":120,"length":240, "sx":0, "sy":0, "data": [1,2,3]}}
		
		dict_test['para']['width'] = int(self.widthSelection.get())
		dict_test['para']['length'] = int(self.lengthSelection.get())
		dict_test['para']['sx'] = int(self.sxSelection.get())
		dict_test['para']['sy'] = int(self.sySelection.get())
		dict_test['id'] = self.getRandomID()
		
		
		json_str = json.dumps(dict_test)
		'''
		self.jsonDataTransfer(json_str)
		
		if self.debug == 1:
			return
		
		#接收应答数据
		json_str = str(sk.recv(2048) , encoding='utf8')
		
		dict_test = json.loads(json_str)
		
		#错误则跳出
		if 'error' in dict_test:
			return
		'''
		#print(len(sendFileData))
		#sk.sendall(sendFileData)
		
		
		
		if self.debug == 2:
			lowerName = self.filename.lower()
			if os.path.splitext(lowerName)[1] == '.png':
				#转换为bmp文件
				im = Image.open(self.filename)
				im = im.convert("RGB")
				#im = im.transpose(Image.FLIP_LEFT_RIGHT)
				im = im.transpose(Image.FLIP_TOP_BOTTOM)
				im.save(lowerName + '.bmp','bmp')
				
				sendFileObj = open(lowerName + '.bmp', 'rb')
		
				sendFileData = sendFileObj.read();
				
				print('covert to bmp')
				
			imageFileLen = len(sendFileData)
			imageDataHead = bytearray([0] * 8)
			imageDataHead[0] = 0x55
			imageDataHead[1] = 0xAA
			
			imageDataHead[4]  = (imageFileLen >>  0) & 0x000000ff;
			imageDataHead[5]  = (imageFileLen >>  8) & 0x000000ff;
			imageDataHead[6]  = (imageFileLen >> 16) & 0x000000ff;
			imageDataHead[7]  = (imageFileLen >> 24) & 0x000000ff;
			
			send_size = 0
			sendFileObj.seek(0)
			a= 0
			while send_size < imageFileLen:
				
				tempData = sendFileObj.read(256)
				imageDataHead[2]  = (len(tempData) >>  0) & 0x000000ff;
				imageDataHead[3]  = (len(tempData) >>  8) & 0x000000ff;
				send_size = send_size + len(tempData)
				#print(imageDataHead+tempData)
				self.serialPort.write((imageDataHead+tempData));
				time.sleep(0.05)
				a = a +1
				print( a)
				
		
		
	def uiRefreshPicture(self):
		
		dict_test = {"id":3433334, "method":"img_refresh", "para":{"width":120,"length":240, "sx":0, "sy":0, "data": [1,2,3]}}
		
		dict_test['para']['width'] = int(self.widthSelection.get())
		dict_test['para']['length'] = int(self.lengthSelection.get())
		dict_test['para']['sx'] = int(self.sxSelection.get())
		dict_test['para']['sy'] = int(self.sySelection.get())
		dict_test['id'] = self.getRandomID()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
		
		
		
		
	def uiBrightness(self):
		dict_test = {"id":3433334, "method":"img_adj_brightness", "para":100 }
		dict_test['id'] = self.getRandomID()
		
		dict_test['para'] = self.brightScale.get()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
		
		
		
	def uiResizePicture(self):
		dict_test = {"id":3433334, "method":"img_resize", "para":50 }
		dict_test['id'] = self.getRandomID()
		
		dict_test['para'] = self.resizeScale.get()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
		
	
		
	def cmdParamSet(self):
		#print(self.cmdTypeSelection.get())
		pass
		
		
	def touchTestFrameCreate(self):
		if self.checkWidgetChanged('Touch') == False:
			return
			
		#self.frame1 = Frame(self.frame)
		
		self.factoryTestButton = Button(self.frame1, text='factory test', command=self.touchFactoryTest, width = 20)
		self.factoryTestButton.grid(row=0, column=0)
		
		self.simuTestButton = Button(self.frame1, text='simu', command=self.touchSimuTest, width = 20)
		self.simuTestButton.grid(row=0, column=1)
		
		
		for i in range(1,5):
			buttonText = "Button" + str(i)
		
			#self.TestButton1 = Button(self.frame1, text='Button1', width = 20,command=lambda s=self, t=buttonText: s.prt(t) )
			#self.TestButton1.grid(row=1, column=0)
			Button(self.frame1, text=buttonText, width = 20,command=lambda s=self, t=buttonText: s.touchButtonPress(t) ).grid(row=i, column=0)
		
		'''
		self.TestButton2 = Button(self.frame1, text='Button2', command=self.touchButtonPress, width = 20)
		self.TestButton2.grid(row=2, column=0)
		self.TestButton3 = Button(self.frame1, text='Button3', command=self.touchButtonPress, width = 20)
		self.TestButton3.grid(row=3, column=0)
		self.TestButton4 = Button(self.frame1, text='Button4', command=self.touchButtonPress, width = 20)
		self.TestButton4.grid(row=4, column=0)
		'''
		
		self.frame1.pack()
		pass
		
	def touchButtonPress(self,text):
		print(text)
		
	def touchFactoryTest(self):
	
		dict_test = {"id":123, "method":"touch_factory_test", "para":"pcba"}
		dict_test['id'] = self.getRandomID()
		
		#dict_test['para'] = self.brightScale.get()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
			
			
	def touchSimuTest(self):
	
		dict_test = {"id":123, "method":"touch_simu", "para":{"type":"up", "speed":100}}
		dict_test['id'] = self.getRandomID()
		
		#dict_test['para'] = self.brightScale.get()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
			
			
			
	def nfcTestFrameCreate(self):
		if self.checkWidgetChanged('NFC') == False:
			return
			
		self.factoryTestButton = Button(self.frame1, text='factory test', command=self.nfcFactoryTest, width = 20)
		self.factoryTestButton.grid(row=0, column=0)
		
		self.nfcTypeList = ['get_cplc','pcba']
		
		self.nfcType = 0
		self.nfcTypeSelection = ttk.Combobox(self.frame1,state ='readonly')
		self.nfcTypeSelection['values'] = self.nfcTypeList
		self.nfcTypeSelection.current(0)
		self.nfcTypeSelection.grid(row=2, column=0)
		
		self.frame1.pack()
		
	def nfcFactoryTest(self):
		dict_test = {"id":123, "method":"nfc_factory_test", "para":" "}
		dict_test['id'] = self.getRandomID()
		dict_test['para'] = self.nfcTypeSelection.get()
		
		#dict_test['para'] = self.brightScale.get()
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
			
	
	def motarTestFrameCreate(self):
		if self.checkWidgetChanged('Motar') == False:
			return
		
		Label(self.frame1,text = "PWM :", width = 20, anchor = 'w').grid(row=0, column=0)
		Label(self.frame1,text = "Duration :", width = 20, anchor = 'w').grid(row=0, column=1)
		
		self.pwmScale = Scale(self.frame1,from_=0, to=100,orient=HORIZONTAL)
		self.pwmScale.grid(row=1,column = 0) 
		self.pwmButton = Button(self.frame1, text='test', command=self.deviceMotarTest, width = 20)
		self.pwmButton.grid(row=2, column=0)#pack(side=RIGHT)
		
		self.motarDurationString = StringVar()
		self.motarDurationString.set('1000')#输入的绑定值
		self.motarDurationSelection = ttk.Entry(self.frame1,textvariable = self.motarDurationString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.motarDurationSelection.grid(row=1, column=1)
			
			
		self.frame1.pack()
		
	def deviceMotarTest(self):
		dict_test = {"id":123, "method":"motar", "para":{"pwm":30, "duration":1000}}
		dict_test['id'] = self.getRandomID()
		
		dict_test['para']['pwm'] = self.pwmScale.get()
		dict_test['para']['duration'] = int(self.motarDurationSelection.get())
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
			
	
	def ledTestFrameCreate(self):
		if self.checkWidgetChanged('Led') == False:
			return
			
		Label(self.frame1,text = "PWM :", width = 20, anchor = 'w').grid(row=0, column=0)
		Label(self.frame1,text = "Duration :", width = 20, anchor = 'w').grid(row=0, column=1)
			
		self.ledScale = Scale(self.frame1,from_=0, to=100,orient=HORIZONTAL)
		self.ledScale.grid(row=1,column = 0) 
		self.ledButton = Button(self.frame1, text='test', command=self.deviceLedTest, width = 20)
		self.ledButton.grid(row=2, column=0)#pack(side=RIGHT)
		
		self.ledDurationString = StringVar()
		self.ledDurationString.set('1000')#输入的绑定值
		self.ledDurationSelection = ttk.Entry(self.frame1,textvariable = self.ledDurationString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.ledDurationSelection.grid(row=1, column=1)
		
		self.frame1.pack()

	def deviceLedTest(self):
		dict_test = {"id":123, "method":"led", "para":{"pwm":30, "duration":1000}}
		dict_test['id'] = self.getRandomID()
		
		dict_test['para']['pwm'] = self.ledScale.get()
		dict_test['para']['duration'] = int(self.ledDurationSelection.get())
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
			
			
			
	def PmTestFrameCreate(self):
		if self.checkWidgetChanged('Power Manage') == False:
			return
			
		self.pmButton = Button(self.frame1, text='Power manage', command=self.devicePmTest, width = 20)
		self.pmButton.grid(row=1, column=0)#pack(side=RIGHT)
		
		self.PmString = StringVar()
		self.PmString.set('0')#输入的绑定值
		self.PmSelection = ttk.Entry(self.frame1,textvariable = self.PmString,validate='key',validatecommand = (self.checkInput,'%P'))
		self.PmSelection.grid(row=0, column=0)
		
		self.frame1.pack()
		
	
	def devicePmTest(self):
		dict_test = {"id":123, "method":"pm_mode", "para":1}
		dict_test['id'] = self.getRandomID()
		
		dict_test['para'] = int(self.PmSelection.get())
		
		json_str = json.dumps(dict_test)
		
		self.jsonDataTransfer(json_str)
		
	def setSerialPort(self, serialPort):	
		self.serialPort = serialPort
		
	def setSocketPort(self,socket):
		self.sk = socket
			
			
'''
sk = socket.socket()

if debug ==1 :
	pass
else :
	sk.connect(("192.168.1.191", 54324))

app = Application()

# 设置窗口标题:
app.frame.title('ryeex test tool')




# 主消息循环:
app.frame.mainloop()



sk.close()

'''


def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', dest='debug', default='0')
	parser.add_argument('--port', dest='port', default='54324')
	parser.add_argument('--IP', dest='IP', default='192.168.1.1')
	parser.add_argument('--serial', dest='serial', default='com6')
	parser.add_argument('--baudrate', dest='baudrate', default='115200')
	
	args = parser.parse_args()
	
	return args


def main():
	args = parse_arguments()
	
	

	sk = socket.socket()

	app = Application(debug = 1)
	
	app.debug = int(args.debug)
	
	debug = int(args.debug)
	
	if debug ==1 :
		pass
	elif debug == 0:
		print('connect IP :%s,  port : %s'%(args.IP, args.port))
		sk.connect((args.IP, int(args.port) ))
		app.setSocketPort(sk)
	elif debug == 2:
		print('serialPort init')
		serialPort = serial.Serial(args.serial, int(args.baudrate), timeout=1)
		app.setSerialPort(serialPort)

	# 设置窗口标题:
	app.frame.title('ryeex test tool')




	# 主消息循环:
	app.frame.mainloop()



	sk.close()
		
		

if __name__ == '__main__':
	main()


































