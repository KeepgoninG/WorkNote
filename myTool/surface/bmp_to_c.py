
from PIL import Image

icon_src = [
    'bmp2c/step.png',
    'bmp2c/cal.png',
    'bmp2c/heart.png',
    'bmp2c/step1.png',

    'bmp2c/m_status_00_msg.bmp',
    'bmp2c/m_status_01_charging.bmp',
    'bmp2c/m_status_02_charging.bmp',
    'bmp2c/m_status_03_forbid.bmp',
    'bmp2c/m_status_offline.bmp',
    'bmp2c/m_status_locked.bmp',

    'bmp2c/loading_1.bmp',
]

'''
(起始坐标x,y, 图片size 宽,高, 前景色r,g,b)
'''
icon_ctrls = [
    (0,0,17,15,255,255,255),
    (0,0,14,18,255,255,255),
    (0,0,17,16,255,255,255),
    (0,0,19,18,255,255,255),

    (0,0,18,18,255,54,57),
    (0,0,18,18,208,2,27),
    (0,0,18,18,23,199,120),
    (0,0,18,18,151,151,151),
    (0,0,18,18,151,151,151),
    (0,0,16,16,151,151,151),

    (0,0,8,8,219,219,219),
]

def load_bmp(filename):
    img = Image.open(filename)
    return img

def get_bmp_range(pic, rect):
    raw = pic.load()
    start_x = rect[0]
    start_y = rect[1]
    w = rect[2]
    h = rect[3]
    alpha_255 = rect[4] + rect[5] + rect[6]
    '''
        1 (1-bit pixels, black and white, stored with one pixel per byte)
        L (8-bit pixels, black and white)
        P (8-bit pixels, mapped to any other mode using a color palette)
        RGB (3x8-bit pixels, true color)
        RGBA (4x8-bit pixels, true color with transparency mask)
        CMYK (4x8-bit pixels, color separation)
        YCbCr (3x8-bit pixels, color video format)
        LAB (3x8-bit pixels, the L*a*b color space)
        HSV (3x8-bit pixels, Hue, Saturation, Value color space)
        I (32-bit signed integer pixels)
        F (32-bit floating point pixels)
    '''
    target_img = Image.new("L", (w,h))
    target_img_data = target_img.load()
    for _x in range(w):
        for _y in range(h):
            x = start_x+_x
            y = start_y+_y
            _raw = raw[x, y]
            r = _raw[0]
            g = _raw[1]
            b = _raw[2]
            alpha_now = (r+g+b)
            if alpha_now > alpha_255:
                alpha_now = alpha_255*255
            else:
                alpha_now = alpha_now*255
            # (r,g,b) = raw[x, y]
            # (r,g,b,_) = raw[x, y]
            # if r+g+b >= (0x100*3/2):
            #     target_img_data[_x, _y] = 0xFF
            # else:
            #     target_img_data[_x, _y] = 0
            target_img_data[_x, _y] = int(alpha_now/alpha_255)

    return target_img

def bmp_8bit_to_c_array(pic, array_name = 'c_array'):
    array_name = array_name.replace("bmp2c/","")
    array_name = array_name.replace(".", '_')
    array_name = array_name.replace(" ", '_')
    c_array = '''static uint8_t const ''' + array_name + '''[] = {
'''
    raw = pic.load()
    (x,y) = pic.size
    for _y in range(y):
        for _x in range(x):
            c_array = c_array + str(raw[_x,_y]) + ', '    
        c_array = c_array + '\n'
    c_array += '};'
    return c_array
    


if __name__ == "__main__":
    # print(icon_ctrls)
    index = 0

    all_c_file = '''

'''

    for i in icon_ctrls:
        img = load_bmp(icon_src[index])
        rect = get_bmp_range(img, i)
        c_array = bmp_8bit_to_c_array(rect, array_name=icon_src[index])
        rect.save(icon_src[index] + ".bmp")
        file_write = open(icon_src[index] + ".c", 'w')
        file_write.write(c_array)
        all_c_file = all_c_file + c_array + '\n'
        file_write.close()
#        print(c_array)
        index = index + 1
#    print(img.size)

    all_file = open('all.c', 'w')
    all_file.write(all_c_file)
    all_file.close
