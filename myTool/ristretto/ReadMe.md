添加输入参数解析
--debug ： 1  打印生成的json，不进行socket连接    0 进行正常连接，通过socket发送json数据    2 ，开启串口直传功能
--IP ： IP 地址（不输入默认值为 192.168.1.1）
--port ： 端口号 （不输入默认值为54324）
--serial 添加串口名 默认为 com8
--baudrate 添加串口的波特率 默认为 115200


例如：
调试：
python ristretto.py --debug 1
使用网络：
python ristretto.py --debug 0 --IP 192.168.1.1 --port 1234
使用串口：
python ristretto.py --debug 2 --serial com8 --baudrate 115200


python ristretto.py --debug 2 --serial com3 --baudrate 115200






























