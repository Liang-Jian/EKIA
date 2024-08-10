# import cv2 as cv
#
# # 读取设备
# cap = cv.VideoCapture('/dev/video0', cv.CAP_V4L)
# # 读取摄像头FPS
# fps = cap.get(cv.CAP_PROP_FPS)
#
# # set dimensions 设置分辨率
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
#
# video = cv.VideoWriter('video.avi', cv.VideoWriter_fourcc('I', '4', '2', '0'), fps, (800, 400)) # 初始化文件写入 文件名 编码解码器 帧率 文件大小
#
# # 录制10帧
# for i in range(100):
#     # take frame 读取帧
#     ret, frame = cap.read()
#     if ret:
#         # write frame to file
#         # cv.imwrite('image-{}.jpg'.format(i), frame)  # 截图
#         video.write(frame) # 录制视频
#
# # release camera 必须要释放摄像头
# cap.release()
import string
import random
# chars = string.ascii_letters + string.digits
# random_str = "".join(random.sample(chars, 10)).lower()
# print(random_str)
import threading
import time

def thread_function(name):
    print(f"线程 {name} 开始运行")
    time.sleep(2)
    print(f"线程 {name} 结束运行")

# 创建并启动线程
thread = threading.Thread(target=thread_function, args=("Thread1",))
thread.start()

# 等待线程结束
thread.join()

# 检查线程是否还活跃
if not thread.is_alive():
    print("线程已死掉，启动一个新的线程")
    # 创建并启动新的线程
    new_thread = threading.Thread(target=thread_function, args=("Thread2",))
    new_thread.start()
    new_thread.join()