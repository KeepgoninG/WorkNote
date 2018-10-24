# readme

## 1. about
本工具使用ufgx的file2c命令工具转换图片文件到.c和.h文件，转换后的文件可直接被romfs文件系统所访问。

## 2. 操作示例：

1. 切换到本file2c.exe所在目录
2. 将图片文件保存在file2c.exe同一目录
3. 在命令行输入转换命令
    file2c -dcs m_data_01_calorie.png m_data_01_calorie.h
4. 将生成的文件m_data_01_calorie.h保存到工程目录里（例如sake工程的resources文件目录为：\resources\img\)


## 3. 应用
sake ugfx中，通过如下方法将新生成的文件应用到工程中
1. include到工程中，在文件“\resources\img\romfs_files.h”
```c
    #include "m_data_01_calorie.h"
```
2. 在工程中通过文件名访问相应的图片（可参考“操作示例.bmp”）
```c
   gdispImageOpenFile(&myImage, "m_data_01_calorie.png");
```

file2c -dcs sake_img_demo\demo_notice_04_2.png demo_notice_04_2.h




