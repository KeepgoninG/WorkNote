
### 环境和依赖

环境 python 3.x

pip install -r requirments.txt

----


初始化的时候根据配置的文件夹枚举所有文件，并尝试分析

然后拖拽log文件，单个文件实时分析

如果需要拓展
在
```python
class singe_file_result_collect(object):

    @staticmethod
    def search_fw_ver(self, l):
        m = singe_file_result_collect.regex_find_fw_ver.findall(l)
        match_count = len(m)
        if match_count > 0:
            self.fw_ver = m[0]

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
    
```
class中增加static 函数，并增加到solve_line方法中

具体实现请查看代码
