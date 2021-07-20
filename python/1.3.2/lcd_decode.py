# encoding:utf-8
# LCD价格数据测试函数

import struct
import sys
from binascii import b2a_hex
from esl_init import log


def zn_number_sml(value):
    '''
        功能：         处理8位控制的7段码屏 18.888|8
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 百分数检查
                    3. 小数检查
                    4. 负数检查
                    5. 格式规约 "{v0:{s0}{a0}{b0}}{dot}{v1:{s1}{a1}{b1}}" s 补全标志 a 对齐方式 b 对齐位数
                    6. 截断处理方式为直接截断无舍入
                    7. 异常处理方式 返回 None

    '''
    if value == '':
        return ''
    for x in value:
        if x not in '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0-_<>.%':
            return None

    ali = "{v0:{s0}{a0}{b0}}{dot}{v1:{s1}{a1}{b1}}"
    pf = False
    l0, l1 = 2, 5

    if '%' in value:
        pf = True
        value = value.rstrip('%')
        ali += '<>|'
        l1 -= 3
    else:
        l1 -= 1

    try:

        if '.' in value:
            V0, V1 = value.split('.')
            if '-' in V0:
                ali = ' -' + ali
                l0 -= 2
            if int(V0) == 0:
                return ali.format(v0='', s0='', a0='>', b0=l0, dot='.', v1=V1[:l1], a1='<', s1='0', b1=l1)
            elif int(V0) < 20 and int(V0) > 0:
                return ali.format(v0=V0, s0='', a0='>', b0=l0, dot='.', v1=V1[:l1], a1='<', s1='0', b1=l1)
            else:
                return None

        else:
            v = int(value)
            if pf:
                if v in range(-99, 0):
                    return ' -' + ali.format(v0='', s0='', a0='', b0='', dot=' ', v1=str(v)[1:], s1=' ', b1=l1, a1='>')
                elif v in range(0, 100):
                    return ali.format(v0='', s0=' ', a0='>', b0='', dot=' ', v1=str(v), s1=' ', b1=l1 + l0, a1='>')
                elif v in range(100, 2000):
                    return ali.format(v0=str(v)[:-2], s0=' ', a0='>', b0=l0, dot=' ', v1=str(v)[-2:], s1=' ', b1=l1, a1='>')
                else:
                    return None
            else:
                if v in range(-9999, 0):
                    return' -' + ali.format(v0='', s0='', a0='', b0='', dot=' ', v1=str(v)[1:], s1=' ', b1=l1, a1='>')
                elif v in range(0, 2000):
                    V = str(v)
                    return ali.format(v0=V[:-2], s0='', a0='>', b0=l0, dot=' ', v1=V[-2:], s1=' ', b1=l1, a1='<')
                elif v in range(2000, 20000):
                    V = str(v)
                    return ali.format(v0=V[:-l1], s0=' ', a0='>', b0=l0, dot=' ', v1=V[-l1:], s1=' ', b1=l1, a1='<')
                elif v in range(20000,  200000):
                    V = str(v)
                    return ali.format(v0=V[:-l1], s0=' ', a0='>', b0=l0, dot=' ', v1=V[-l1:], s1=' ', b1=l1, a1='<')
                else:
                    return None

    except Exception, e:
        return None
    return None


def zn_number_big(value):
    '''
        功能：         处理6位控制的7段码屏 1888|8
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 百分数检查
                    3. 小数检查
                    4. 负数检查
                    5. 格式规约 "{v:{s}{a}{b}}" s 补全标志 a 对齐方式 b 对齐位数
                    6. 截断处理方式为直接截断无舍入
                    7. 异常处理方式 返回 None
    '''

    if value == '':
        return ''
    for x in value:
        if x not in '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0-_<>.%':
            return None

    ali = "{v:{s}{a}{b}}"
    pf = False
    length = 6

    if '.' in value:
        return None

    if '%' in value:
        pf = True
        value = value.rstrip('%')
        ali += '<>|'
        length -= 3
    else:
        length -= 1

    try:
        num = int(value)
        if num < 0:
            ali = ' -' + ali
            length -= 2
    except Exception, e:
        return None

    if not pf:
        if not (num in range(-999, 20000)):
            return None
    else:
        if num < 0:
            if not (num in range(-9, 0)):
                return None
        else:
            if not (num in range(0, 200)):
                return None

    return ali.format(v=str(abs(num)), s=' ', a='>', b=length)


def zn_mark_state(value):
    '''
        功能：         处理5位控制的状态码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in 'ldxscLDXSC ':
            return None
    return value


def zn_mark_curren(value):
    '''
        功能：         处理4位控制的货币码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in '1234 ':
            return None
    return value


def zn_mark_arrow(value):
    '''
        功能：         处理3位控制的箭头码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in 'aduADU ':
            return None
    return value


def zn_mark_promo(value):
    '''
        功能：         处理1位控制的促销码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in 'anrANR ':
            return None
    return value


def zn_mark_bar(value):
    '''
        功能：         处理4位控制的红条码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in '1234ABCDabcd':
            return None
    return value


def zn_mark_unit(value):
    '''
        功能：         处理4位控制的单位码屏 
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 异常处理方式 返回 None
    '''
    if value == '':
        return ''

    for x in value:
        if x not in 'GLKUglku ':
            return None
    return value


def zn_alpha(value):
    '''
        功能：         处理9位控制的11段码屏 88.8.8.88
        主要过程：
                    1. 检查原始输入中是否有无法翻译字符<合法性检查>
                    2. 分隔符检查
                    3. 长度检查
                    4. 负数检查
                    5. 格式规约 
                        "{0: ^6}"
                        "{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}"
                        "{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}"
                        "{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}{0[3]:{1}{2}{6}}""
                    6. 截断处理方式为直接截断无舍入
                    7. 异常处理方式 返回 None

    '''
    if value == '':
        return ''

    mid = '{0: ^6}'
    for x in value:
        if x not in '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0-_*<>.':
            return None

    if value.count('.') > 0:
        st = value.split('.')
    else:
        return mid.format(value) + '   '

    length = len(st)

    if length == 2:
        ali = "{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}"
        if len(st[0]) > len(st[1]):
            v0, v1 = 4, 2
            ali += '  .'
        elif len(st[0]) < len(st[1]):
            v0, v1 = 2, 4
            ali += '.  '
        else:
            v0, v1 = 3, 3
            ali += ' . '
        return ali.format(st, '0', '>', v0, v1)
    elif length == 3:
        ali = "{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}"
        if len(st[1]) > 2 or len(st[1]) == 0:
            return None
        elif len(st[0]) == len(st[2]):
            v0, v1, v2 = 2, 2, 2
            ali += '. .'
        elif len(st[0]) > len(st[2]):
            v0, v1, v2 = 3, 1, 2
            ali += ' ..'
        elif len(st[0]) < len(st[2]):
            v0, v1, v2 = 2, 1, 3
            ali += '.. '
        return ali.format(st, '0', '>', v0, v1, v2)
    elif length == 4:
        ali = '{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}{0[3]:{1}{2}{6}}' + '...'
        if len(st[1]) > 1 or len(st[2]) > 1:
            return None
        else:
            v0, v1, v2, v3 = 2, 1, 1, 2
            return ali.format(st, '0', '>', v0, v1, v2, v3)
    else:
        return None


def _get_led_config(led_config):
    '''
    led_num, t0, t1, t2, cnt
    '''
    led_color_map = {"GREEN": 0, "BLUE": 1, "RED": 2}

    led_num, t0, t1, t2, count =  int(led_color_map[led_config['color']]), \
        int(led_config['on_time']), int(led_config['off_time']),\
        int(led_config['sleep_time']), int(led_config['count'])

    fmt = '<BBBHH'
    d = struct.pack(fmt, led_num, t0, t1, t2, count)
    return d


def get_led_config(i, t):
    '''
    led_num, t0, t1, t2, cnt
    '''
    led_config = t['led_config_map'][t[i['op3']][i['op4']]['led_config']]
    return _get_led_config(led_config)


def get_rc(i, t):
    '''
    page_flag, page_id, time, led_flag, led_config
    '''
    page_id = int(t[i['op3']][i['op4']]['rc_config']['rc_page_id'])

    rf_config_mode = t[i['op3']][i['op4']]['rc_config']['rc_config_mode']
    rc_config_mode = t['rc_config_mode_map'][rf_config_mode]

    page_flag = int(rc_config_mode['page_flag'])
    times = int(rc_config_mode['time'])
    led_flag = int(rc_config_mode['led_flag'])
    fmt = '<BBHB'
    d = struct.pack(fmt, page_flag, page_id, times, led_flag)

    led_config = rc_config_mode['led_config']
    led_config = t['led_config_map'][led_config]
    d += _get_led_config(led_config)

    return d


def get_value(zone, i):
    '''
        功能：         向上提供统一获取模版刷新数据方法 
        主要过程：
                    1. 检查数据源  非 None 表示数据来源为数据库 None表示来源模版
                    2. 自省获得函数handler 并传参调用
        异常：         
                    1. 可能引发的异常主要是传入非ASCII值
                    2. 自定义zone没有编写对应的处理方法
        异常处理： 
                    log提示获得值失败
                    并返回None
    '''
    try:

        if zone['title'] in ['None', 'NONE', 'none', None]:
            return eval(zone.get('area'))(zone.get('value'))
        return eval(zone.get('area'))(str(i[zone['title']]))

    except Exception, e:
        log.warning("get_value error %s", e)
        return None


def filed(zone):
    if zone['title'] in ['None', 'NONE', 'none', None]:
        return zone['value']
    else:
        return zone['title']


def get_seg_data(i, t):
    '''
        功能：         向上提供统一打包半成品数据流的方法
        主要过程：
                    1. 获取需要打包eslid, version, security_code, magnet, led_t, seg_rc, zone patch, module path, seg_page_t等信息
                    2. 将值和对应的zone模版打包                   
        异常：         
                    1. 获取值失败 得到None
                    2. 自定义zone没有编写对应的处理方法
        异常处理： 
                    获取值失败 得到None 结束打包过程返回None
    '''
    fmt = '>IBBBBB'

    pages = t[i['op3']][i['op4']].get('pages')

    d = struct.pack("B", len(pages) if pages else 0)

    for p in pages:
        page_id, mask, scroll, zone_num = p['page_id'], p[
            'mask'], p['scroll'], len(p['data'])
        d += struct.pack("BBBB", page_id, mask, scroll, zone_num)
        for zone in p['data']:
            v = str(get_value(zone, i))
            if v == 'None':
                log.warning('%s,%s', t.get('eslid'), filed(zone))
                return None
            z = str(zone["area"])
            d += struct.pack("32s64s", z, v)

    return d


def get_test_data():

    esl_info = {'eslid': '59-12-09-99', 'version': '0', 'security_code': '0', 'magnet': '0',
                'op3': 'HS_EL_5300', 'op4': 'demo', 'Price': 1, 'Price1': 2, 'Price2': 3, 'Price3': 4, "op5": "{'screen_type': 'HS_EL_5300', 'module_path': './config/zone/bm_sn-HS_EL_5300-30.json', 'version': 1, 'zone_path': './config/zone/zn_sn-HS_EL_5300-30.json'}"
                }

    temp = {
        "HS_EL_5300": {
            "demo": {
                "led_config": "RED_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3",
                "rc_config": {"rc_page_id": "1", "rc_config_mode": "RC_CONFIG_MODE_1"},
                "pages": [
                    {"page_id": 0, "mask": 0, "scroll": 1, "data": [
                        {"title": "NONE", "value": "-0.9%",
                            "area": "zn_number_big"},
                        {"title": "NONE", "value": "4587", "area": "zn_number_sml"},
                        {"title": "NONE", "value": "ABCDEF", "area": "zn_alpha"},
                        {"title": "NONE", "value": "2", "area": "zn_mark_curren"},
                        {"title": "NONE", "value": "1", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "", "area": "zn_mark_promo"}
                    ]},
                    {"page_id": 1, "mask": 0, "scroll": 1, "data": [
                        {"title": "NONE", "value": "", "area": "zn_number_big"},
                        {"title": "NONE", "value": "asd", "area": "zn_number_sml"},
                        {"title": "NONE", "value": "GH.I.J.KL", "area": "zn_alpha"},
                        {"title": "NONE", "value": "1", "area": "zn_mark_curren"},
                        {"title": "NONE", "value": "2", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "P", "area": "zn_mark_promo"}
                    ]},
                    {"page_id": 2, "mask": 0, "scroll": 1, "data": [
                        {"title": "NONE", "value": "-0.45%",
                            "area": "zn_number_big"},
                        {"title": "NONE", "value": "", "area": "zn_number_sml"},
                        {"title": "NONE", "value": "MNOPQR", "area": "zn_alpha"},
                        {"title": "NONE", "value": "3", "area": "zn_mark_curren"},
                        {"title": "NONE", "value": "3", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "r", "area": "zn_mark_promo"}
                    ]},
                    {"page_id": 3, "mask": 0, "scroll": 1, "data": [
                        {"title": "NONE", "value": "", "area": "zn_number_big"},
                        {"title": "NONE", "value": "24", "area": "zn_number_sml"},
                        {"title": "NONE", "value": "STUVWX", "area": "zn_alpha"},
                        {"title": "NONE", "value": "24", "area": "zn_mark_curren"},
                        {"title": "NONE", "value": "4", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "a", "area": "zn_mark_promo"}
                    ]},
                    {"page_id": 4, "mask": 0, "scroll": 1, "data": [
                        {"title": "NONE", "value": "", "area": "zn_number_big"},
                        {"title": "NONE", "value": "10", "area": "zn_number_sml"},
                        {"title": "NONE", "value": "ZZZZZZ", "area": "zn_alpha"},
                        {"title": "NONE", "value": "1", "area": "zn_mark_curren"},
                        {"title": "NONE", "value": "B", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "n", "area": "zn_mark_promo"}
                    ]},
                    {"page_id": 8, "mask": 1, "scroll": 0, "data": [
                        {"title": "NONE", "value": "4", "area": "zn_mark_bar"},
                        {"title": "NONE", "value": "a", "area": "zn_mark_promo"}
                    ]}
                ]
            }
        },
        "zone_path": "./config/zone/zn_sn-1130.json",
        "module_path": "./config/zone/bm_sn-1130.json",
        "led_config_map": {
            "RED_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3":
                {"color": "RED", "on_time": 30, "off_time": 30,
                    "sleep_time": 3, "count": 3},
            "BLUE_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3":
                {"color": "BLUE", "on_time": 30, "off_time": 30,
                    "sleep_time": 3, "count": 3},
            "GREEN_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3":
                {"color": "GREEN", "on_time": 30,
                    "off_time": 30, "sleep_time": 3, "count": 3},
            "BLUE_ON_20ms_OFF_20ms_SLEEP_0s_COUNT_20":
                {"color": "BLUE", "on_time": 20, "off_time": 20,
                    "sleep_time": 0, "count": 20},
            "RED_ON_10ms_OFF_20ms_SLEEP_20s_COUNT_5":
                {"color": "RED", "on_time": 10, "off_time": 20,
                    "sleep_time": 254, "count": 5},
            "GREEN_ON_3ms_OFF_3ms_SLEEP_20s_COUNT_10":
                {"color": "GREEN", "on_time": 1, "off_time": 1,
                    "sleep_time": 20, "count": 10},
            "BLUE_ON_4ms_OFF_2ms_SLEEP_0s_COUNT_255":
                {"color": "BLUE", "on_time": 4, "off_time": 2,
                    "sleep_time": 0, "count": 255},
            "GRED_ON_2ms_OFF_1ms_SLEEP_0s_COUNT_20":
                {"color": "RED", "on_time": 2, "off_time": 1,
                    "sleep_time": 0, "count": 20},
            "GREEN_ON_1ms_OFF_1ms_SLEEP_5s_COUNT_10":
                {"color": "GREEN", "on_time": 1, "off_time": 1,
                    "sleep_time": 5, "count": 10},
            "GREEN_ON_8ms_OFF_4ms_SLEEP_0s_COUNT_10":
                {"color": "GREEN", "on_time": 8, "off_time": 4,
                    "sleep_time": 0, "count": 10}
        },
        "rc_config_mode_map": {
            "RC_CONFIG_MODE_1": {"page_flag": 0, "time": 256, "led_flag": 1,
                                 "led_config": "GREEN_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3"}
        }
    }

    return esl_info, temp


def send_seg_data(i, t):
    eslid = int(i['eslid'].replace('-', ''), 16)
    version = int(i.get('version', 1))
    security_code = int(i.get('security_code', 0xfa58))
    magnet = int(i.get('magnet', 0x0f0f))

    try:
        o5 = eval(i.get("op5"), {}, {})
        zone_path = str(o5.get("zone_path"))
        module_path = str(o5.get("module_path"))
        if not (zone_path and module_path):
            return None
        fmt = '>IB'
        d = struct.pack(fmt, eslid, version)
        fmt = '<HH'
        d += struct.pack(fmt, security_code, magnet)
        d += get_led_config(i, t)
        d += get_rc(i, t)
        fmt = '64s64s'
        d += struct.pack(fmt, zone_path, module_path)
        d += get_seg_data(i, t)

    except KeyError, e:
        log.warning('op5 missing in db %s' % e)
        return None
    except Exception, e:
        log.warning('invalid input during packaging data,ganna end this task')
        return None

    return d


def make_test_data():
    w = sys.stdout.write

    esl_info, temp = get_test_data()

    d = struct.pack("<H", 1)
    d += send_seg_data(esl_info, temp)
    w(d)


def valid_test_data(function):
    import random
    func = eval(function)
    b = random.random()
    for x in [0.01, 0.1, 1, 10, 100]:
        a = b * x
        print '原数:%s\t负数:%s\t负百分:%s\t百分:%s' % (str(a), '-' + str(a), '-' + str(a) + '%', str(a) + '%')
        print '%s\t\t\t%s\t\t\t%s\t\t\t%s' % (func(str(a)), func('-' + str(a)), func('-' + str(a) + '%'), func(str(a) + '%'))
        print ' '

if __name__ == '__main__':
    make_test_data()
    # valid_test_data('zn_number_sml')
    # valid_test_data('zn_number_big')
    # zn_number_big('N')
    # zn_number_sml('N')
