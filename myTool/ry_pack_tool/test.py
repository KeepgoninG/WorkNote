import ctypes
from ctypes import *


ll = ctypes.cdll.LoadLibrary
lib = ll("./libLoader.so")
#lib = ll("./libloader_win64.so")


file = c_char_p(b'test3')
lib.inputJsonFile.argtypes = [c_char_p]
lib.inputJsonFile( file)


lib.test_py()

f = open('test3','rb')

json_string = f.read();

j_str = c_char_p(json_string)

lib.inputJsonString(j_str)