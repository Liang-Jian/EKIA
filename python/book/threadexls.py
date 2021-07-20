import os
import multiprocessing as mp

filename = "123.txt"
cores = 5


def process_wrapper(chunkStart, chunkSize):
    num = 0
    with open(filename) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:num +=1

    return num

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

pool = mp.Pool(cores)
jobs = []

for chunkStart, chunkSize in chunkify(filename):
    jobs.append(pool.apply_async(process_wrapper, (chunkStart,chunkSize)))

res = []
for job in jobs:
    res.append(job.get())

pool.close()
print(sum(res))
