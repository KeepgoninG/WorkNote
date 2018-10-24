import json

def surface_item_template_0():
    items = []
    item = {}
    item['type']='data'
    item['name'] = "hour"
    item['pos'] = {'x':6,"y":28}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name'] = "minute"
    item['pos'] = {'x':6,"y":68}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name'] ="dayofmonth"
    item['pos'] = {'x':6,"y":113}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name'] ="week"
    item['pos'] = {'x':34,"y":112}
    item['font']={"type":2, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="steps"
    item['pos'] = {'x':65,"y":171}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name'] ="hrm"
    item['pos'] = {'x':65,"y":195}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="cal"
    item['pos'] = {'x':65,"y":219}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    return items

def surface_item_template_1():
    items = []
    item = {}
    item['type']='data'
    item['name']="hour"
    item['pos'] = {'x':2,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']=":"
    item['pos'] = {'x':50,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="minute"
    item['pos'] = {'x':62,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    
    item = {}
    item['type']='data'
    item['name']="month"
    item['pos'] = {'x':6,"y":92}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']="."
    item['pos'] = {'x':28,"y":92}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="dayofmonth"
    item['pos'] = {'x':34,"y":92}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="week"
    item['pos'] = {'x':72,"y":92}
    item['font']={"type":2, "size":16, "color":16777215}
    items.append(item)

    item = {}
    item['type']='data'
    item['name']="steps"
    item['pos'] = {'x':52,"y":202}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    return items

def surface_item_template_2():
    items = []
    item = {}
    item['type']='data'
    item['name']="hour"
    item['pos'] = {'x':36,"y":57}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="minute"
    item['pos'] = {'x':36,"y":96}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    
    item = {}
    item['type']='data'
    item['name']="dayofmonth"
    item['pos'] = {'x':29,"y":136}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="week"
    item['pos'] = {'x':55,"y":137}
    item['font']={"type":2, "size":16, "color":16777215}
    items.append(item)

    item = {}
    item['type']='data'
    item['name']="steps"
    item['pos'] = {'x':68,"y":200}
    item['font']={"type":1, "size":20, "color":16777215}
    item['style']={"alignment":'middle'}
    items.append(item)
    return items

def surface_item_template_3():
    items = []
    item = {}
    item['type']='data'
    item['name']="hour"
    item['pos'] = {'x':2,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']=":"
    item['pos'] = {'x':52,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="minute"
    item['pos'] = {'x':62,"y":44}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    
    item = {}
    item['type']='data'
    item['name']="month"
    item['pos'] = {'x':6,"y":92}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']="."
    item['pos'] = {'x':28,"y":92}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="dayofmonth"
    item['pos'] = {'x':34,"y":92}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="week"
    item['pos'] = {'x':72,"y":92}
    item['font']={"type":2, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="steps"
    item['pos'] = {'x':60,"y":192}
    item['font']={"type":1, "size":20, "color":16777215}
    item['style']={"alignment":'middle'}
    items.append(item)
    return items

def surface_item_template_0_with_icon():
    items = surface_item_template_0()
    item = {}
    item['type']='icon'
    item['name']="step.ico"
    item['pos'] = {'x':46,"y":173}
    item['style'] = {'color':16777215}
    items.append(item)
    item = {}
    item['type']='icon'
    item['name']="hrm.ico"
    item['pos'] = {'x':46,"y":197}
    item['style'] = {'color':16777215}
    items.append(item)
    item = {}
    item['type']='icon'
    item['name']="cal.ico"
    item['pos'] = {'x':47,"y":219}
    item['style'] = {'color':16777215}
    items.append(item)
    return items

def surface_item_template_1_with_icon():
    items = surface_item_template_1()
    item = {}
    item['type']='icon'
    item['name']="step1.ico"
    item['pos'] = {'x':25,"y":201}
    item['style'] = {'color':16777215}
    items.append(item)
    return items
    
def surface_item_template_2_with_icon():
    items = surface_item_template_2()
    item = {}
    item['type']='icon'
    item['name']="step.ico"
    item['pos'] = {'x':29,"y":202}
    item['style'] = {'color':16777215}
    items.append(item)
    return items

def surface_item_template_1_more_space():
    items = []
    item = {}
    item['type']='data'
    item['name']="hour"
    item['pos'] = {'x':6,"y":30}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']=":"
    item['pos'] = {'x':54,"y":30}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="minute"
    item['pos'] = {'x':66,"y":30}
    item['font']={"type":1, "size":44, "color":16777215}
    items.append(item)
    
    item = {}
    item['type']='data'
    item['name']="month"
    item['pos'] = {'x':6,"y":78}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='symbol'
    item['name']="."
    item['pos'] = {'x':28,"y":78}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="dayofmonth"
    item['pos'] = {'x':34,"y":78}
    item['font']={"type":1, "size":16, "color":16777215}
    items.append(item)
    item = {}
    item['type']='data'
    item['name']="week"
    item['pos'] = {'x':72,"y":78}
    item['font']={"type":2, "size":16, "color":16777215}
    items.append(item)

    item = {}
    item['type']='data'
    item['name']="steps"
    item['pos'] = {'x':44,"y":218}
    item['font']={"type":1, "size":20, "color":16777215}
    items.append(item)
    item = {}
    item['type']='icon'
    item['name']="step.ico"
    item['pos'] = {'x':25,"y":219}
    item['style'] = {'color':16777215}
    items.append(item)
    return items

def get_red_arron_dic():
    default_surface_target = {}
    default_surface_target['id'] = 1
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.surface.redarrow"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_01_red_arron.bmp"
    default_surface_target['item']=surface_item_template_0()
    return default_surface_target

def get_earth():
    default_surface_target = {}
    default_surface_target['id'] = 2
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.system.earth"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_earth.bmp"
    default_surface_target['item']=surface_item_template_1()
    return default_surface_target

def get_galaxy():
    default_surface_target = {}
    default_surface_target['id'] = 3
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.system.galaxy"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_galaxy.bmp"
    default_surface_target['item']=surface_item_template_3()
    return default_surface_target

def get_colorful():
    default_surface_target = {}
    default_surface_target['id'] = 4
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.surface.colorful"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_colorful.bmp"

    default_surface_target['item']=surface_item_template_2()
    return default_surface_target

def get_red_curve():
    default_surface_target = {}
    default_surface_target['id'] = 5
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.surface.redcurve"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_redcurve.bmp"
    default_surface_target['item']=surface_item_template_0()
    return default_surface_target

def get_green_curve():
    default_surface_target = {}
    default_surface_target['id'] = 6
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "ryeex.surface.greencurve"
    default_surface_target['author'] = "ryeex"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "surface_greencurve.bmp"
    default_surface_target['item']=surface_item_template_0()
    return default_surface_target

def get_user_template_0():
    default_surface_target = {}
    default_surface_target['id'] = 0
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "user.surface.id0"
    default_surface_target['author'] = "0"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "s_user_id0.bmp"
    default_surface_target['item']=surface_item_template_0_with_icon()
    return default_surface_target

def get_user_template_1():
    default_surface_target = {}
    default_surface_target['id'] = 0
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "user.surface.id0"
    default_surface_target['author'] = "0"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "s_user_id0.bmp"
    default_surface_target['item']=surface_item_template_1_with_icon()
    return default_surface_target

def get_user_template_2():
    default_surface_target = {}
    default_surface_target['id'] = 0
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "user.surface.id0"
    default_surface_target['author'] = "0"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "s_user_id0.bmp"
    default_surface_target['item']=surface_item_template_2_with_icon()
    return default_surface_target


def get_user_template_more_space():
    default_surface_target = {}
    default_surface_target['id'] = 0
    default_surface_target['model']="ryeex.band.sake.v1"
    default_surface_target['name'] = "user.surface.id0"
    default_surface_target['author'] = "0"
    default_surface_target['version'] = 1
    default_surface_target['bg_pic'] = "s_user_id0.bmp"
    default_surface_target['item']=surface_item_template_1_more_space()
    return default_surface_target

def func_prepare_c_string(s):
    tmp = s
    tmp = tmp.replace('"', '\\\"')
    tmp = tmp.replace('\n', '\\\n')
    return tmp


if __name__ == "__main__":
    default_surfaces = [
        get_red_arron_dic(),    # template 0
        get_earth(),
        get_galaxy(),
        get_colorful(),
        get_red_curve(),        # template 0
        get_green_curve(),      # template 0
    ]
    # default_surfaces = [
    #     get_user_template_0(),    # template 0
    #     get_earth(),
    #     get_galaxy(),
    #     get_colorful(),
    #     get_user_template_1(),
    #     get_user_template_2(),
    # ]

    default_user_template = [
        get_user_template_0(),
#        get_user_template_1(),
        get_user_template_more_space(),
        get_user_template_2(),
    ]
    c_default_jsons_array = '''char const* pp_default_surface[] = {
'''

    json_defaults = []
    total_size = 0
    for s in default_surfaces:
        j_dev = json.dumps(s)
        j_dev = j_dev.replace(" ", "")
        # j_log = json.dumps(s, indent=4)
        total_size = total_size + len(j_dev)
        json_defaults.append(j_dev)
        c_default_jsons_array = c_default_jsons_array + "\""
        c_default_jsons_array = c_default_jsons_array + func_prepare_c_string(j_dev)
        c_default_jsons_array = c_default_jsons_array + "\",\n"
    c_default_jsons_array = c_default_jsons_array + "};"

    file_write = open("surface_defaults_json.c", 'w')
    file_write.write(c_default_jsons_array)
    file_write.close()
    print("default_jsons: " + str(total_size))

    json_templates = []
    for s in default_user_template:
        j_template = json.dumps(s)
        j_template = j_template.replace(" ", "")
        json_templates.append(j_template)
    
    index = 0
    for j in json_templates:
        file_template = open("template"+str(index)+".json", "w")
        file_template.write(j)
        file_template.close()
        index = index + 1

    index = 1
    for j in json_defaults:
        file_template = open("s_0_"+str(index)+".json", "w")
        file_template.write(j)
        file_template.close()
        index = index + 1