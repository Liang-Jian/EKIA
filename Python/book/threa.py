import time
import threading
# start = time.perf_counter()
# def do_something():
#     print("Sleeping 1 second")
#     time.sleep(1)
#     print("Done Sleeping")
# do_something()
# do_something()
#
# finish = time.perf_counter()
#
# print(f'Finished in {round(finish-start,2)} second(s)')
#########################
#
# start = time.perf_counter()
# def do_something():
#     print("Sleeping 1 second")
#     time.sleep(1)
#     print("Done Sleeping")
# t1 = threading.Thread(target=do_something,args=())
# t2 = threading.Thread(target=do_something,args=())
# t1.start()
# t2.start()
# finish = time.perf_counter()
# print(f'Finished in {round(finish-start,2)} second(s)')
#######################

# start = time.perf_counter()
# def do_something():
#     print("Sleeping 1 second")
#     time.sleep(1)
#     print("Done Sleeping")
# t1 = threading.Thread(target=do_something,args=())
# t2 = threading.Thread(target=do_something,args=())
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# finish = time.perf_counter()
# print(f'Finished in {round(finish-start,2)} second(s)')

########################
import concurrent.futures

import concurrent.futures.thread
start = time.perf_counter()
def do_something(timers):
    print(f'Sleep {timers} seconds(s) ...')
    time.sleep(timers)
    # print('Done sleeping')
    return f'done sleeping... {timers}'
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     result = [executor.submit(do_something,1) for _ in range(10) ]
#     for f in concurrent.futures.as_completed(result):
#         print(f.result())
    # f1 = executor.submit(do_something,1)
    # f2 = executor.submit(do_something,1)
    # print(f1.result())
    # print(f2.result())
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     secs = [5,4,3,2,1]
#     results = [executor.submit(do_something,sec) for sec in secs ]
#     for f in concurrent.futures.as_completed(results):
#         print(f.result())
#
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     secs = [5,4,3,2,1]
#     results = executor.map(do_something,secs)
#     for result in results:
#         print(result)
# finish = time.perf_counter()
# print(f'Finished in {round(finish-start,2)} second(s)')


###############

import requests
import time
import concurrent.futures


img_urls = [
    "https://img.lexus.com.cn/images/es-gallery-no-1-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-2-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-3-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-4-180716-566x400.jpg",
    "https://img.lexus.com.cn/images/es-gallery-no-25-180716-566x400.jpg",
]
t1 = time.perf_counter()
def download_image(img_url):
    img_byte = requests.get(img_url).content
    img_name1 = img_url.split('/')[4]
    img_name = f'{img_name1}.jpg'
    with open(img_name,'wb') as img_file:
        img_file.write(img_byte)
        print(f'{img_name} was  downloaded ...')

with concurrent.futures.ThreadPoolExecutor() as excutor:
    excutor.map(download_image,img_urls)

# for i in img_urls:
#     download_image(i)
t2  = time.perf_counter()

print(f'findinsh time {t2 - t1} second')