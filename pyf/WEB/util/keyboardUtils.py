import win32api
import win32con

class KeyboardKeys(object):
    '''
    模拟键盘按键类
    '''
    VK_CODE = \
        {
        'enter':0x0D,
        'ctrl': 0x11,
        'v': 0x56,
        '1': 0x31,
        '2': 0x32
        }
    @staticmethod
    def key_down(keyName):
        '''
        按下按键
        '''
        win32api.keybd_event(KeyboardKeys.VK_CODE[keyName], 0 , 0 ,0)

    @staticmethod
    def key_up(keyName):
        '''
        释放按键
        '''
        win32api.keybd_event(KeyboardKeys.VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def one_key(key):
        '''
        模拟单个按键
        '''
        KeyboardKeys.key_down(key)
        KeyboardKeys.key_up(key)

    @staticmethod
    def two_keys(key1, key2):
        '''
        模拟两个组合按键
        '''
        KeyboardKeys.key_down(key1)
        KeyboardKeys.key_down(key2)
        KeyboardKeys.key_up(key1)
        KeyboardKeys.key_up(key2)