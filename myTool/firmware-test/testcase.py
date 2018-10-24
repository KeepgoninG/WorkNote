#coding=utf-8

import unittest
import serial
import json
import time
import HTMLTestRunner
import random
import socket
import  binascii


class Test(unittest.TestCase):

    def setserialPort(self,id,method,para):
        json_str = json.dumps({"id": id, "method": method, "para": para})
        print(json_str)
        self.serialPort.write(bytes(json_str, encoding="utf8"))
        b = self.serialPort.read(2000)
        # print(b)
        return json.loads(b)

    def getRandomID(self):
        # self.testFunctionFlag = 80
        # randomStart = self.testFunctionFlag * 100
        # randomEnd = randomStart + 99
        return random.randint(0, 100000000)

    def setUp(self):
         self.serialPort = serial.Serial("com5", 115200, timeout=1)
         print('serialPort init')

        #获取版本号
    def test_version(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "version")
        print(serialPortresult)
        self.assertEqual('result' in serialPortresult, True)

        #获取SN
    def test_SN(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "sn")
        print("SN:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)

        #获取did
    def test_did(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "did")
        print("did:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)

        #获取mac
    def test_mac(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "mac")
        print("mac:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)

        #获取hex_conf
    def test_hex_conf(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "hex_conf")
        print("hex_conf:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)

    def test_Gsensor(self):
        paralist = ['on', 'off']
        for para in paralist:
           randomid = self.getRandomID()
           serialPortresult = self.setserialPort(randomid, "gsensor", para)
           self.assertEqual(serialPortresult['result'], 'ok')
           print(serialPortresult)
           time.sleep(0.5)

    def test_update(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "get_device_info", "update")
        print(serialPortresult)


    def test_Gsensor_E(self):
        paralist = ["get"] #无效参数
        for para in paralist:
            randomid = self.getRandomID()
            serialPortresult = self.setserialPort(randomid, "gsensor", para)
            # print(serialPortresult)
            self.assertEqual('error' in serialPortresult, True)

    def test_Gsenson_getid(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "gsensor", "get_id")
        print("Gsenson_id:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)
        # result = int(serialPortresult['result'])
        # self.assertGreaterEqual(result, 0)
        # self.assertLessEqual(result, 100000)


    # def test_Gsenson_getxyz(self):
    #     randomid = self.getRandomID()
    #     serialPortresult = self.setserialPort(randomid, "gsensor", "get_value")
    #     print("Gsensor_xyz:", serialPortresult)


    def test_HeartRate(self):
     # for i in range(1):
        paralist = ['on', 'off']
        for a in paralist:
            c = self.getRandomID()
            serialPortresult = self.setserialPort(c, "heartrate", a)
            print("Heartrate-----------", serialPortresult)
            self.assertEqual(serialPortresult['result'] and serialPortresult['id'], 'ok' and c)
            time.sleep(0.5)

    def test_HeartRate_E(self):
        # for i in range(2):
            paralist = [-1, 101, 'h#j']  # 无效参数
            for para in paralist:
                randomid = self.getRandomID()
                serialPortresult = self.setserialPort(randomid, "heartrate", para)
                print(serialPortresult)
                self.assertEqual('error' in serialPortresult, True)

    def test_HeartRate_getid(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "heartrate", "get_id")
        print("Gsenson_id:", serialPortresult)
        self.assertEqual('result' in serialPortresult, True)


    # def test_HeartRate_getxyz(self):
    #     randomid = self.getRandomID()
    #     serialPortresult = self.setserialPort(randomid, "heartrate", "get_value")
    #     print(serialPortresult)
        # result = serialPortresult['result']
        # print(result)
        # s = int(result)
        # # self.assertGreaterEqual(s, 40)
        # # self.assertLessEqual(s, 100000)

    def test_Nfc(self):
       # for i in range(1):
        paralist = ['on', 'off']
        for a in paralist:
            randomid = self.getRandomID()
            serialPortresult = self.setserialPort(randomid, "nfc", a)
            self.assertEqual(serialPortresult['result'] and serialPortresult['id'], 'ok' and randomid)
            print(serialPortresult)
            time.sleep(0.5)

    def test_Nfc_E(self):
        paralist = [-1, 101, 'h#j'] #无效参数
        for a in paralist:
            randomid = self.getRandomID()
            serialPortresult = self.setserialPort(randomid, "nfc", a)
            self.assertEqual('error' in serialPortresult, True)

    # def test_Nfc_getid(self):
    #     randomid = self.getRandomID()
    #     serialPortresult = self.setserialPort(randomid, "nfc", "get_id")
    #     print("nfc_id:", serialPortresult)

    # def test_Nfc_getxyz(self):
    #     randomid = self.getRandomID()
    #     serialPortresult = self.setserialPort(randomid, "nfc", "get_value")
    #     print("nfc_xyz", serialPortresult)
    #
    # def test_Vibrator(self):
    #     paralist = ['on', 'off']
    #     for a in paralist:
    #         randomid = self.getRandomID()
    #         serialPortresult = self.setserialPort(randomid, "vibrator", a)
    #         print(serialPortresult)
    #         self.assertEqual(serialPortresult['result'] and serialPortresult['id'], 'ok' and randomid)
    #
    # def test_Vibrator_E(self):
    #     paralist = [-1, 101, 'h#j'] #无效参数
    #     for a in paralist:
    #         randomid = self.getRandomID()
    #         serialPortresult = self.setserialPort(randomid, "vibrator", a)
    #
    #         self.assertEqual('error' in serialPortresult, True)

    # def test_Ble(self):
    #     randomid = self.getRandomID()
    #     serialPortresult = self.setserialPort(randomid, "ble", 'get_version')
    #     print(serialPortresult)

    def test_Spiflash_getid(self):
        randomid = self.getRandomID()
        serialPortresult = self.setserialPort(randomid, "exflash", "get_id")
        print(serialPortresult)
        self.assertEqual('result' in serialPortresult, True)


    def test_oled(self):
        paralist = ['on', 'off', {"set_rgb": 1233434}]
        for a in paralist:
            randomid = self.getRandomID()
            serialPortresult = self.setserialPort(randomid, "oled", a)
            self.assertEqual(serialPortresult['result'] and serialPortresult['id'], 'ok' and randomid)
            print(serialPortresult)

    def test_touch(self):
        paralist = ['on', 'off']
        for a in paralist:
            randomid = self.getRandomID()
            serialPortresult = self.setserialPort(randomid, "touch", a)
            print(serialPortresult)
            self.assertEqual(serialPortresult['result'] and serialPortresult['id'], 'ok' and randomid)

    # def test_touchpanel_E(self):
    #     paralist = [-1, 101, 'h#j'] #无效参数
    #     for a in paralist:
    #         serialPortresult = self.setserialPort(11111, "touchpanel", a)
    #         self.assertEqual('error' in serialPortresult,True)
    #
    # def test_touchpanel_getid(self):
    #         serialPortresult = self.setserialPort(1, "touchpanel", "get_id")
    #         print(serialPortresult)
    #
    # def test_touchpanel_getxyz(self):
    #         serialPortresult = self.setserialPort(2, "touchpanel", "get_value")
    #         print(serialPortresult)

    def tearDown(self):
        self.serialPort.close()


if __name__ == '__main__':
     # unittest.main()

     testunit = unittest.TestSuite()
     for i in range(10):
     # testunit.addTest(Test('test_version'))
     # testunit.addTest(Test('test_SN'))
     # testunit.addTest(Test('test_did'))
     # testunit.addTest(Test('test_mac'))
     # testunit.addTest(Test('test_hex_conf'))
        testunit.addTest(Test('test_Gsensor'))
        testunit.addTest(Test('test_Gsenson_getid'))
        testunit.addTest(Test('test_HeartRate_getid'))
        testunit.addTest(Test('test_HeartRate'))
        testunit.addTest(Test('test_Spiflash_getid'))
        testunit.addTest(Test('test_oled'))
        testunit.addTest(Test('test_touch'))
        testunit.addTest(Test('test_Nfc'))


     HtmlFile = "D:\\TestReport\\myreport.html"
     # 将结果写入该文件
     fp = open(HtmlFile, "wb")
     runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'sake', description=u"测试结果详情",verbosity=2)

     runner.run(testunit)

