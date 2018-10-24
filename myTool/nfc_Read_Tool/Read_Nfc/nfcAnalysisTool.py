import zipfile
import os
import re
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

'''hexArry = ("30","31","32","33","34","35","36","37","38","39",\
			"41","42","43","44","45","46","47","48","49","4A",\
			"4B","4C","4D","4E","4F","50","51","52","53","54",\
			"55","56","57","58","59","5A")
			
strArry = ("0","1","2","3","4","5","6","7","8","9",\
			"A","B","C","D","E","F","G","H","I","J",\
			"K","L","M","N","O","P","Q","R","S","T",\
			"U","V","W","X","Y","Z")'''

	
	
			
f=open('readbin.txt','r')
alllines=f.readlines()
f1=open('new.txt','w')
f.close()

flag = 0

for eachline in alllines:
	flag = eachline.find("00008000")
	if flag:
		if eachline.find("00008010") == 0 or \
			eachline.find("00008100") == 0 or eachline.find("00008080") == 0 or eachline.find("000FF800") == 0 or \
			eachline.find("000FF804") == 0 or eachline.find("000FF814") == 0 or eachline.find("000FF824") == 0 or \
			eachline.find("000FF832") == 0 or eachline.find("000FF842") == 0 or eachline.find("000FF852") == 0 or \
			eachline.find("000FF860") == 0 or eachline.find("000FF870") == 0 or eachline.find("000FF880") == 0 or \
			eachline.find("000FF88E") == 0 or eachline.find("000FF89E") == 0 or eachline.find("000FF8AE") == 0 or \
			eachline.find("000FF8BC") == 0 or eachline.find("000FF8CC") == 0 or eachline.find("000FF8DC") == 0:
			f1.writelines(eachline)
		continue
	else:
		f1.writelines(eachline)
	
f1.close()

f2=open('new.txt','r')
lines=f2.readlines()
f2.close()

f3=open('123.txt','w')
for line in lines:
	line = line.replace("00008000", "DID") 
	line = line.replace("00008100", "MAC") 
	line = line.replace("00008080", "SN") 
	line = line.replace("000FF800", "cardN") 
	line = line.replace("000FF804", "card") 
	line = line.replace("000FF832", "card") 
	line = line.replace("000FF860", "card") 
	line = line.replace("000FF88E", "card") 
	line = line.replace("000FF8BC", "card") 
	f3.write(line)
	
f3.close()

f4=open('123.txt','r')
f4lines=f4.readlines()
f4.close()

f5=open('456.txt','w')
for line4 in f4lines:
	s=line4.replace(' ','')
	s=s.replace('FF','')
	s=s.replace('535A542E57414C4C45542E454E56','深圳通')
	s=s.replace('5943542E55534552','岭南通')
	s=s.replace('9156000014010001','北京通')
	s=s.replace('A00000063201010510009156000014A1','京津冀')
	s=s.replace('A0000053425748544B','武汉通')
	s=s.replace('4351515041592E5359533331','重庆畅通卡')
	s=s.replace('A000000632010105215053555A484F55','江苏一卡通')
	s=s.replace('A0000000037100869807010000000000','长安通')
	s=s.replace('A0000000032300869807010000000000','合肥通')
	s=s.replace('A00000063201010553004755414E4758','广西通')
	s=s.replace('A0000006320101051320004A494C494E','吉林通')
	s=s.replace('00','')
	#print(s)
	if len(s) > 7:
		if s.find("DID") == 0:
			f5.write('\n')
		f5.write(s)
		
	#print(len(s))
    #a = filter(lambda ch: ch not in " ", line4) 
    #f5.writelines(a)
	
f5.close()


# DID=3739313935
regex_find_did = re.compile('''DID=(\d\w+)''')
regex_find_sn = re.compile('''SN=(\d\w+)''')
regex_find_cardNum = re.compile('''cardN=(\d\w+)''')
regex_find_card = re.compile('''card=(\d+)''')
regex_find_numRow = re.compile('''(\d+)=''')


def replace_did(line):
    result = line
    m = regex_find_did.findall(line)
    if len(m) > 0:
        ascii_str = m[0]
        result = "DID=" + bytearray.fromhex(ascii_str).decode() + "\n"
    return result
    
def replace_sn(line):
    result = line
    m = regex_find_sn.findall(line)
    if len(m) > 0:
        ascii_str = m[0]
        result = "SN=" + bytearray.fromhex(ascii_str).decode() + "\n"
    return result
	
def replace_cardNum(line):
    result = line
    m = regex_find_cardNum.findall(line)
    if len(m) > 0:
            if m[0] == '01' or m[0] == '02' or\
               m[0] == '03' or m[0] == '04' or\
               m[0] == '05':
                  result = "cardNum=" + m[0] + "\n"
            else:
                  result = ""
            #print(m[0])

    return result

def replace_card(line):
    result = line
    m = regex_find_card.findall(line)
    if len(m) > 0:
            result = ""
            #print(m)

    return result


def replace_delrow(line):
    result = line
    m = regex_find_numRow.findall(line)
    if len(m) > 0:
            result = ""
            #print(m[0])

    return result

	
lines = open('456.txt').readlines()
#print(lines)
result = []
for l in lines:
    l = replace_did(l)
    l = replace_sn(l)
    l = replace_cardNum(l)
    l = replace_card(l)
    l = replace_delrow(l)
    result.append(l)


r = open('userNfcData.txt', 'w')
for rr in result:
    r.write(rr)

r.close()


filename = '123.txt'
os.remove(filename)
  
filename = '456.txt'
os.remove(filename)

filename = 'new.txt'
os.remove(filename)



'''
f6=open('456.txt','r')
f6lines=f6.readlines()
f6.close()
didCount = [0,2,4,6,8]
snCount  = [0,2,4,6,8,10,12,14,16,18,20,22]
indexCount = 0

for count in f6lines:
        str1 = ""
        str2 = ""
        indexCount = 0
        if count.find("DID") == 0:
                print(count)
                for jj in didCount:
                        str1 = count[jj+4:jj+6:1]
                        #print(str1)
                        for kk in range(35):
                                if hexArry[kk] == str1:
                                        str2 = str2 + strArry[kk]
                                        indexCount = indexCount + 1
                                        if indexCount == 5:
                                                print(str2)
        if count.find("SN") == 0:
                print(count)
                indexCount = 0
                for ii in snCount:
                        str1 = count[ii+3:ii+5:1]
                        #print(str1)
                        for ll in range(35):
                                if hexArry[ll] == str1:
                                        str2 = str2 + strArry[ll]
                                        indexCount = indexCount + 1
                                        if indexCount == 11:
                                                print(str2)
                                        
'''


#print("stop!")
#input("<Enter end>")




