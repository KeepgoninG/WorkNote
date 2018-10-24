
import urllib3
import urllib
import re
import threadpool
import os

urllib3.disable_warnings()

FILE_LIST_NAME = 'log_file_list.txt'
MULTI_THREAD_CTRL = 40

DOWNLOAD_PATH_DIR = "download"

# remote_urls = [
#     'https://heyplus-pub.oss-cn-hangzhou.aliyuncs.com/feedback/device_operation_21838_20181001015405_aAZmXE8JX4zSGB4J.zip',
#     'https://heyplus-pub.oss-cn-hangzhou.aliyuncs.com/feedback/device_connect_32889_20181001002515_5slx5NQEhThZDarJ.zip',
#     'https://heyplus-pub.oss-cn-hangzhou.aliyuncs.com/feedback/健康运动_31946_20181001004821_1uvlGJeJoE2IzejI.zip',
#     'https://heyplus-pub.oss-cn-hangzhou.aliyuncs.com/feedback/else_19006_20181001004925_r1QduQFiO1jdqgSG.zip',
# ]

re_find_file_name = re.compile('''.*\/(\w+.zip)''')
current_count = 0
total_count = 0

def getFileName(s):
    global re_find_file_name
    r = re_find_file_name.findall(s)
    if len(r) == 1:
        return r[0]
    else:
        return ""
    
def url_clean(s):
    return urllib.parse.quote(s.replace("\n", "")).replace("%3A",":")

def fetch_single_url(url):
    global current_count
    global total_count
    file_name = getFileName(url)
    if file_name == "":
        return
    else:
        local_file = DOWNLOAD_PATH_DIR + "/" + file_name
        real_url = url_clean(url)
        resp = http.request('GET', real_url)
        with open(local_file,'wb') as f:
            f.write(resp.data)
            f.close()
        print("downlowd finished " + str(current_count) + '''/'''+ str(total_count))
        current_count = current_count + 1

if __name__ == "__main__":
    remote_urls = open(FILE_LIST_NAME).readlines()

    total_count = len(remote_urls)
    print("total count: " + str(total_count))

    http = urllib3.PoolManager(num_pools=MULTI_THREAD_CTRL)
    pool = threadpool.ThreadPool(MULTI_THREAD_CTRL)

    if os.path.exists(DOWNLOAD_PATH_DIR):
        pass
    else:
        os.mkdir(DOWNLOAD_PATH_DIR)

    requests = threadpool.makeRequests(fetch_single_url, remote_urls) 
    
    [pool.putRequest(req) for req in requests]
    pool.wait()
    
    print("all finished\r\n")
