import multiprocessing ,time


# t1 = time.perf_counter()
# def do_something():
#     print('sleeping 1 second')
#     time.sleep(3)
#     print('donw sleeped')
# # do_something()
# # do_something()
# for _ in range(10):
#     p =multiprocessing.Process(target=do_something)
#     p.start()
#
#
# t2 = time.perf_counter()
# print(f'findish {t2 -t1} second (s)')

#######################
# t1 = time.perf_counter()
# def do_something(second):
#     print(f'sleeping {second} second')
#     time.sleep(second)
#     print('down sleeped')
#
# PRo = []
# for _ in range(10):
#     p = multiprocessing.Process(target=do_something,args=[3])
#     p.start()
#     PRo.append(p)
# for p in PRo:
#     p.join()
# t2 = time.perf_counter()
# print(f'findish {t2 -t1} second (s)')


######################
# import concurrent.futures
# t1 = time.perf_counter()
# def do_something(second):
#     print(f'sleeping {second} second')
#     time.sleep(second)
#     # print('down sleeped')
#     return 'done sleeped'
# # do_something()
# # do_something()
#
#
# secs = [5,4,3,2,1]
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     # f1 = executor.submit(do_something,1.5)
#     # print(f1.result())
#     result = [executor.submit(do_something,sec ) for sec in secs]
#     for f in concurrent.futures.as_completed(result):
#         print(f.result())
#
# t2 = time.perf_counter()
# print(f'findish {t2 -t1} second (s)')


##########################
# import concurrent.futures
# t1 = time.perf_counter()
# def do_something(second):
#     print(f'sleeping {second} second')
#     time.sleep(second)
#     return 'done sleeped'
# secs = [5,4,3,2,1]
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     secs=[5,4,3,2,1]
#     result = executor.map(do_something,secs)
#     for p in result:
#         print(p)
#
# t2 = time.perf_counter()
# print(f'findish {t2 -t1} second (s)')
###########
# import time
# from PIL import Image,ImageFilter
# img_names =[
# 'es-gallery-no-1-180716-566x400.jpg.jpg',
# 'es-gallery-no-2-180716-566x400.jpg.jpg',
# 'es-gallery-no-3-180716-566x400.jpg.jpg',
# 'es-gallery-no-4-180716-566x400.jpg.jpg',
# 'es-gallery-no-25-180716-566x400.jpg.jpg'
# ]
#
# t1 = time.perf_counter()
# size = (1200,1200)
# for img_name in img_names:
#     img = Image.open(img_name)
#     img = img.filter(ImageFilter.GaussianBlur(10))
#     img.thumbnail(size)
#     img.save(f'processed {img_name}')
#     print(f'{img_name} was processed...')
# t2 = time.perf_counter()
# print(f'findish {t2 -t1} second (s)')
###############################################
import time
import concurrent.futures
from PIL import Image,ImageFilter
img_names =[
'es-gallery-no-1-180716-566x400.jpg.jpg',
'es-gallery-no-2-180716-566x400.jpg.jpg',
'es-gallery-no-3-180716-566x400.jpg.jpg',
'es-gallery-no-4-180716-566x400.jpg.jpg',
'es-gallery-no-25-180716-566x400.jpg.jpg'
]

# t1 = time.perf_counter()
# size = (1200,1200)
# def process_image(img_name):
# # for img_name in img_names:
#     img = Image.open(img_name)
#     img = img.filter(ImageFilter.GaussianBlur(10))
#     img.thumbnail(size)
#     img.save(f'processed {img_name}')
#     print(f'{img_name} was processed...')
'''
import requests
img_urls = [
    "https://img.lexus.com.cn/images/es-gallery-no-1-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-2-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-3-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-4-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-25-180716-566x400.jpg",
]

def download_image(img_url):
    img_byte = requests.get(img_url).content
    img_name = img_url.split('/')[4]
    img_name = f'{img_name}.jpg'
    with open(img_name,'wb') as img_file:
        img_file.write(img_byte)
        print(f'{img_name} was  downloaded ...')

if __name__ == '__main__':
    t1 = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download_image, img_urls)

    t2 = time.perf_counter()
    print(f'findish {t2 -t1} second (s)')
'''


def fuck():
    print("Fuck")


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(fuck)