# share data  use queue
import queue,threading
# q = queue.Queue()
# q = queue.LifoQueue()
# for i in range(10):
#     prioritaet = i % 3
#     q.put((prioritaet,i))
# for i in range(10):
#     print(q.get())

#################
#
# q = queue.Queue()
# num_worker =4
# def do_work(item):
#     print(item)
# def worker():
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         do_work(item)
#         q.task_done()
# threads = []
# for i in range(num_worker):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)
# for i in range(100):
#     q.put(i)
# for i in range(num_worker):
#     q.put(None)
# for i in threads:
#     i.join()
#############################
# import multiprocessing,queue
# def calc_squre(numbers,q):
#     for n in numbers:
#         q.put(n*n)
# if __name__ == '__main__':
#     numbers = [2,3,5]
#     q = multiprocessing.Queue()
#     p = multiprocessing.Process(target=calc_squre,args=(numbers,q))
#     p.start()
#     p.join()
#     while q.empty() is False:
#         print(q.get())
#######################


# def bytestostr():
#     s = b'\xe3\x80\x90\xe6\xb5\x81\xe9\x87\x8f\xe6\x8f\x90\xe9\x86\x92\xe3\x80\x91'
#     print(str(s, encoding='utf-8'))
def calc_squre(numbers,result):
    for idx,n in enumerate(numbers):
        result[idx] = n * n
        print(result[idx])
# calc_squre(2,4)

