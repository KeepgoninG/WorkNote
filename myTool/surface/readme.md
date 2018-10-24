
## 使用环境

python 
> 3.x

依赖库
> pip install -r requirements.txt

----
## 图片转换

适用于单色bmp或者png, 带透明度转换成
```C
typedef struct
{
    uint8_t const* p_data;
    uint16_t width;
    uint16_t height;
    uint32_t fgcolor;   //未直接使用
}raw_png_descript_t;

void draw_raw_png_to_framebuffer(raw_png_descript_t const* p_pic, uint16_t x, uint16_t y, uint32_t color);

```
可用的格式

相关代码:**bmp_to_c.py**

#### 直接使用流程
1. 将图片复制到bmp2c文件夹
2. 将路径更新到脚本数组中
```python
icon_src = []
```
3. 将需要转换的图片描述更新到描述数组中
```python
'''
(起始坐标x,y, 图片size 宽,高, 前景色r,g,b)
'''
icon_ctrls = []
```

4. 运行脚本，将自动在bmp2c中生成临时文件，并更新all.c
请注意临时文件不要上传git

----
json生成

#### 说明
没什么好说的，看代码吧。。
自动生成json的模板
和默认表盘的json
脚本中已经做了json最小化处理

