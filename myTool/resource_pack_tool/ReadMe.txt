打包OTA用的资源文件，通过new_des.c编译过来生成res_pack.exe
使用的编译器为gcc

使用方法：
		res_pack.exe    资源文件路径
		
例如：
		res_pack.exe   .\data  
		
		
最后会生成res_pack.bin文件，用于OTA

其中资源文件路径下的clear_list.txt中的文件将会被解析为要删除的文件，每个文件名占用一行















