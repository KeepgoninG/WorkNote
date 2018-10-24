

#用来打包文件

from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRC32 import CRC32
from PyCRC.CRCCCITT import CRCCCITT
import threading
import sys
import os

#GUI tkinter 相关
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog



from ctypes import c_uint32





sendDataBuf = bytearray(1024 * 10)



filename = ''

'''
input = b'\x01\x02\x03'
#print(CRCCCITT().calculate(input))

#input = b'\x01'
print(CRC16().calculate(input))
print(CRC16DNP().calculate(input))
print(CRC16Kermit().calculate(input))
print(CRC16SICK().calculate(input))
print(CRC32().calculate(input))
print(CRCCCITT().calculate(input))
'''

class Application():
	def __init__(self, master=None):
		self.frame = Tk()
		self.frame.geometry('300x300')
		self.packFileName = ''
		self.packFilePath = '.'
		self.filename = ''
		self.versionNumber = 0
		self.dataStartAddr = 64
		self.crcValue = 0
		self.reserveDataSize = 44
		
		self.fileHeaderBuf = bytearray(64)
		
		self.createWidgets()
		
		
	def createWidgets(self):
		#self.nameInput = Entry(self)
		#self.nameInput.pack()
		
		
		#按键部分,选择文件和打包文件
		self.frame1 = Frame(self.frame)
		self.openFileButton = Button(self.frame1, text='Open file', command=self.openFile)
		self.openFileButton.pack(side=LEFT)
		
		self.packFileButton = Button(self.frame1, text='pack file', command=self.packFile)
		self.packFileButton.pack(side=RIGHT)
		self.frame1.pack(side = TOP)
		
		#文件类型选择部分
		self.fileTypeText =  Label(self.frame,text = "类型:")
		self.fileTypeText.pack()
		
		#self.text_fileType = Text(self.frame,height = "1")
		#self.text_fileType.pack(side=RIGHT)
		#self.fileTypeList = Listbox(self.frame,)
		self.fileTypeitem = {'boot':1,'firmware':2,'font':3,'App data':4,'App file':5}
		#for typeName in self.fileTypeitem:
		#	self.fileTypeList.insert(END,typeName)
		#self.fileTypeList.pack()
		
		self.fileType = 0
		#self.fileTypeSelection = ttk.Combobox(self.frame,command = self.setFileType)
		self.fileTypeSelection = ttk.Combobox(self.frame,state ='readonly')
		self.fileTypeSelection['values'] = ['boot','firmware','font','App data','App file']
		self.fileTypeSelection.current(0)
		self.fileTypeSelection.pack()
		
		
		
		#勾选部分,选择是否使用CRC
		
		self.crcEnable = BooleanVar()
		self.crcCheck = Checkbutton(self.frame,text = "CRC",variable = self.crcEnable, command = self.crcCheckButton)
		self.crcCheck.pack()
		
		
		#版本号设置
		self.frame2 = Frame(self.frame)
		
		self.versionText =  Label(self.frame2,text = '版本号 : ')
		self.versionText.pack(side = LEFT)
		#self.versionSet = Entry(self.frame2,text = '版本号 : ')
		#self.versionSet.pack(side = RIGHT)
		
		self.versionHigh = ttk.Combobox(self.frame2)
		self.versionHigh['values'] = [0,1,2,3,4,5,6,7,8,9]
		self.versionHigh.current(0)
		self.versionHigh.pack()
		
		self.versionMid = ttk.Combobox(self.frame2)
		self.versionMid['values'] = [0,1,2,3,4,5,6,7,8,9]
		self.versionMid.current(0)
		self.versionMid.pack()
		
		self.versionLow = ttk.Combobox(self.frame2)
		self.versionLow['values'] = [0,1,2,3,4,5,6,7,8,9]
		self.versionLow.current(0)
		self.versionLow.pack()
		
		self.frame2.pack()
		
		#设置pack的文件名
		
		self.packFileNameSet = Entry(self.frame2)
		#self.packFileNameSet.set('')
		self.packFileNameSet.pack()
		
		
		
	

	def openFile(self):
		self.filename = tkinter.filedialog.askopenfilename(title='打开文件',filetypes=[('All Files', '*')])
		#print(self.filename)
		#onlyFileName = os.path.split(self.filename)[1]
		#print(onlyFileName)
		self.frame.title('ryeex ' + self.filename)
		#self.packFileNameSet.set('')
		
	def packFile(self):
		if self.filename == '':
			#print('file name is NUll')
			messagebox.showinfo('ERROR','文件名为空\n file name is NULL')
		else:
			#print(self.filename)
			
			
			#创建新文件
			if self.packFileNameSet.get() == '':
				onlyFileName = os.path.split(self.filename)[1]
				packFileName = onlyFileName + '.ry'
				#packFileObject = open(os.path.join(self.packFilePath,packFileName), 'wb')
			else :
				packFileName = self.packFileNameSet.get() + '.ry'
				
			packFileObject = open(os.path.join(self.packFilePath,packFileName), 'wb')
			
			#设置文件头部
			#1.文件大小
			fileObject = open(self.filename,'rb')
			fileSize = fileObject.seek(0,os.SEEK_END)
			#print(fileSize)
			#tempbuf = buffer(self.fileHeaderBuf, 0, 4)
			packFileObject.write( bytes((c_uint32(fileSize))) )
			
			#2.设置数据起始位置
			packFileObject.write( bytes((c_uint32(self.dataStartAddr))) )
			
			#3.设置类型
			self.fileType = self.fileTypeitem[self.fileTypeSelection.get()]
			packFileObject.write( bytes((c_uint32(self.fileType))) )
			
			#4.设置CRC校验
			fileObject.seek(0, os.SEEK_SET)
			self.crcValue = int(CRCCCITT().calculate(fileObject.read()))
			print(self.crcValue)
			if self.crcEnable.get() == TRUE:
				pass #进行CRC校验
			packFileObject.write( bytes((c_uint32(self.crcValue))) )
			
			
			
			#5.设置版本号
			self.getVersionNumber()
			packFileObject.write( bytes((c_uint32(self.versionNumber))) )
			
			#6.设置保留位
			for x in range(self.reserveDataSize):
				packFileObject.write(b'0')
			
			
			#7.写入数据
			fileObject.seek(0, os.SEEK_SET)
			packFileObject.write(fileObject.read())
			
			
			
	def crcCheckButton(self):
		#print(self.crcEnable.get())
		self.fileType = self.fileTypeitem[self.fileTypeSelection.get()]
		#print(self.fileType)
		
		
	def setFileType(self):
		self.fileType = self.fileTypeitem[self.fileTypeSelection.get()]
		#print(self.fileType)
		
	def getVersionNumber(self):
		self.versionNumber = int(self.versionHigh.get())*100 + int(self.versionMid.get())*10 + int(self.versionLow.get())
		#print(self.versionNumber)
		return self.versionNumber
			
			
		

#master = Tk()
#master.height = 1000
app = Application()

# 设置窗口标题:
app.frame.title('ryeex ')
# 主消息循环:
app.frame.mainloop()