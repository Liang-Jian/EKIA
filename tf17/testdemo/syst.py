from ctypes import *
import time
import os
import win32api
class dd_input():
    def __init__(self):
        parentDirPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print(parentDirPath)
        path = parentDirPath + ("\\dll\\DD81200x64.64.dll")
        print(path)
        self.dd_dll = windll.LoadLibrary(path)

        # DD虚拟码，可以用DD内置函数转换。
        self.vk = {'5': 205, 'c': 503, 'n': 506, 'z': 501, '3': 203, '1': 201, 'd': 403, '0': 210, 'l': 409, '8': 208, 'w': 302,
            'u': 307, '4': 204, 'e': 303, '[': 311, 'f': 404, 'y': 306, 'x': 502, 'g': 405, 'v': 504, 'r': 304, 'i': 308,
            'a': 401, 'm': 507, 'h': 406, '.': 509, ',': 508, ']': 312, '/': 510, '6': 206, '2': 202, 'b': 505, 'k': 408,
            '7': 207, 'q': 301, "'": 411, '\\': 313, 'j': 407, '`': 200, '9': 209, 'p': 310, 'o': 309, 't': 305, '-': 211,
            '=': 212, 's': 402, ';': 410}
        # 需要组合shift的按键。
        self.vk2 = {'"': "'", '#': '3', ')': '0', '^': '6', '?': '/', '>': '.', '<': ',', '+': '=', '*': '8', '&': '7', '{': '[', '_': '-',
            '|': '\\', '~': '`', ':': ';', '$': '4', '}': ']', '%': '5', '@': '2', '!': '1', '(': '9'}

    def down_up(self, code):
        # 进行一组按键。
        self.dd_dll.DD_key(self.vk[code], 1)
        self.dd_dll.DD_key(self.vk[code], 2)

    def dd(self, i):
        # 500是shift键码。
        if i.isupper():
            # 如果是一个大写的玩意。

            # 按下抬起。
            self.dd_dll.DD_key(500, 1)
            self.down_up(i.lower())
            self.dd_dll.DD_key(500, 2)

        elif i in '~!@#$%^&*()_+{}|:"<>?':
            # 如果是需要这样按键的玩意。
            self.dd_dll.DD_key(500, 1)
            self.down_up(self.vk2[i])
            self.dd_dll.DD_key(500, 2)
        else:
            self.dd_dll.DD_key(203, 1)
            self.dd_dll.DD_key(203, 1)
            self.dd_dll.DD_key(203, 1)
            self.dd_dll.DD_key(203, 1)
            self.dd_dll.DD_key(203, 1)
            self.dd_dll.DD_key(203, 1)
            # # self.dd_dll.DD_key(206, 1)
            # # self.dd_dll.DD_key(204, 1)
            # # self.dd_dll.DD_key(202, 1)
            # # self.dd_dll.DD_key(203, 1)
            # # self.dd_dll.DD_key(205, 1)
            # # self.dd_dll.DD_key(209, 1)

    # input("按任意键继续...")
    # 之后等待两秒。
    time.sleep(2)
    # 测试按键。

    # 释放dll
    def shifang(self):
        win32api.FreeLibrary(self.dd_dll._handle)
if __name__ == "__main__":
    dd_input = dd_input()
    for i in '3642359':
        dd_input.dd(i)
        for i in '3642359':
            dd_input.dd(i)
        dd_input.shifang()