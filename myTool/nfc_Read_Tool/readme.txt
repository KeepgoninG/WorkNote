文件夹nfc_TRead_Tool:
	功能：bat通过jlink.exe软件读取指定地址指定长度的数据；
	注意：readTool中的jlink路径需要根据不通的pc的安装路径进行修改，jlink工具的SN也好根据不通设备修改
	读取的结果会保存到Read_Nfc文件夹中的readbin.txt中
	
nfcAnalysisTool：
	功能：将readbin中的数据处理，只保留设备的DID、MAC、SN、开卡数、卡类型，并存放在userNfcData.txt中