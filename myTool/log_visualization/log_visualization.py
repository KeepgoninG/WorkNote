
import zipfile
import os
import re

source_dir = "download"

class singe_file_result_collect(object):
    regex_find_surface_install_timeout = re.compile('''\[surface_add\] timeout abort process''')
    regex_find_fw_ver = re.compile('''\[E\] fwVer: (\d+\.\d+\.\d+), ''')
    regex_find_surface_install_space_error = re.compile('''\[surface_add\] fs no enough memory''')
    regex_find_fs_space_error = re.compile('''\[surface\] all dir size total:(\d+), free:(\d+) files:(\d+)''')

    def __init__(self, _name = ""):
        self.final_result = ""
        self.transmit_timeout = 0
        self.fs_size_error = 0
        self.install_size_err = 0
        self.fw_ver = "not found"
        self.err_counter = 0
        self.lines = []
        self.name = _name
        
    @staticmethod
    def solve_timeout_by_line(self, l):
        match_count = len(singe_file_result_collect.regex_find_surface_install_timeout.findall(l))
        if match_count > 0:
            # print("传输超时")
            self.err_counter = self.err_counter + 1
            self.transmit_timeout = self.transmit_timeout + 1

    @staticmethod
    def search_fw_ver(self, l):
        m = singe_file_result_collect.regex_find_fw_ver.findall(l)
        match_count = len(m)
        if match_count > 0:
            self.fw_ver = m[0]

    @staticmethod
    def solve_surface_install_size_error_by_line(self, l):
        match_count = len(singe_file_result_collect.regex_find_surface_install_space_error.findall(l))
        if match_count > 0:
            # print("空间不足")
            self.err_counter = self.err_counter + 1
            self.install_size_err = self.install_size_err + 1

    @staticmethod
    def solve_filesystem_size_error_by_line(self, l):
        ms = singe_file_result_collect.regex_find_fs_space_error.findall(l)
        match_count = len(ms)
        if match_count > 0:
            for m in ms:
                if int(m[0]) + int(m[1]) < 6000000:
                    self.err_counter = self.err_counter + 1
                    self.fs_size_error = self.fs_size_error + 1
    
    def solve_lines(self, _lines):
        self.lines = _lines
        '''
        按行处理，需要扩展则自行添加
        '''
        self.err_counter = 0
        for l in self.lines:
            l_str = l.decode('utf8')
            singe_file_result_collect.solve_timeout_by_line(self, l_str)
            singe_file_result_collect.solve_surface_install_size_error_by_line(self, l_str)
            singe_file_result_collect.solve_filesystem_size_error_by_line(self, l_str)
            singe_file_result_collect.search_fw_ver(self, l_str)
    
    def print_result(self):
        if self.err_counter == 0:
            self.final_result = "\r\n未从日志中分析出异常\r\n\r\n"
        if self.transmit_timeout > 0:
            self.final_result = self.final_result + "\r\n传输超时\r\n"
        if self.install_size_err > 0:
            self.final_result = self.final_result + "\r\n疑似文件系统空间异常\r\n"
        self.final_result = self.final_result + "\r\nfwVer:"+ self.fw_ver +"\r\n"
        print(self.final_result)

class all_file_result_collect(object):
    def __init__(self):
        self.files = []
        self._invalid_zip = 0
        self._no_device_log = 0
        self._valid_device_log = 0
        self._fs_size_err = 0
        self._surface_transmit_timeout = 0
        self._known_err_files = 0
        self._surface_install_size_err = 0
        self._print_file_result = False
        self._timeout_dic = dict()

    def addfileResult(self, result):
        self.files.append(result)
        if result.fs_size_error != 0:
            self._fs_size_err = self._fs_size_err + 1
        if result.install_size_err != 0:
            if result.fs_size_error == 0:
                self._surface_install_size_err = self._surface_install_size_err + 1
        if result.transmit_timeout != 0:
            self._surface_transmit_timeout = self._surface_transmit_timeout + 1
            if result.fw_ver in self._timeout_dic.keys():
                self._timeout_dic[result.fw_ver] = self._timeout_dic[result.fw_ver] + 1
            else:
                self._timeout_dic[result.fw_ver] = 1
        if result.err_counter != 0:
            self._known_err_files = self._known_err_files + 1        

    
    def invalid_zip_file(self):
        self._invalid_zip = self._invalid_zip + 1

    def no_dev_log(self):
        self._no_device_log = self._no_device_log + 1

    def dumpTotalResult(self):
        print("总计压缩包:" + str(len(self.files)))
        print("文件系统空间异常:" + str(self._fs_size_err))
        print("安装表盘空间异常[疑似文件系统]:" + str(self._surface_install_size_err))
        print("传输超时:" + str(self._surface_transmit_timeout) + str(self._timeout_dic))
        print("查找到已知错误:" + str(self._known_err_files))
        print("无效压缩包:" + str(self._invalid_zip))
        print("没有设备日志:" + str(self._no_device_log))


def check_single_file(file_name, total):
    global total_visual
    try:             
        with zipfile.ZipFile(file_name) as z:
            raw_file = ""
            files = z.namelist()
            file_count = len(files)
            if file_count == 0:
                print("空压缩包")

            if file_count == 1:
    #            print("单文件压缩包")
                raw_file = files[0]
            if file_count > 1:
                for f in files:
                    if str.find(f, '_dev_') > 0:
#                    print("多文件压缩包")
                        raw_file = f
                        break
            if raw_file != "":   
                raw = z.open(raw_file).readlines()
                s = singe_file_result_collect(_name=file_name)
                s.solve_lines(raw)
                total.addfileResult(s)
                if total._print_file_result:
                    s.print_result()
            else:
                total.no_dev_log()
    except zipfile.BadZipFile:
        total.invalid_zip_file()
        print("Bad zip file:" + file_name )

if __name__ == "__main__":
    print('''用户反馈日志分析，目前仅支持几种错误原因定位''')
    
    all_files = os.listdir(source_dir)
    # print(all_files)
    
    # all_files = all_files[:300:]

    files = []

    for f in all_files:
        files.append(source_dir + "/" + f)

    total_visual = all_file_result_collect()

    for f in files:
        check_single_file(f, total_visual)
    
    if len(files) > 0:
        total_visual.dumpTotalResult()

    manual = all_file_result_collect()
    manual._print_file_result = True
    while True:
        text = input("请输入文件完整路径，支持拖拽，输入 'q' 退出:\n" )
        raw = ""
        if text is "q":
            break
        if text == "":
            continue
        if os.path.isfile(text):
            print("输入的路径: " + text)
            check_single_file(text, manual)
        else:
            print("无效路径")
            continue

    manual.dumpTotalResult()
        
