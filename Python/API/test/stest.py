import os
def deleteFile(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            deleteFile(itemsrc)
    #     try:
    #         os.rmdir(src)
    #     except:
    #         pass


if __name__ == '__main__':
    dirname = r'D:\ol-test\interface-auto-testing\autodata\resultfile\新建文本文档.txt'
    # dirname =
    # print(dirname)
    # print(deleteFile(os.path.abspath('../')+ r"\autodata\resultfile"))
    # print(deleteFile(os.path.abspath('../')+ r"\autodata\resultfile\"))
    print(deleteFile(dirname))