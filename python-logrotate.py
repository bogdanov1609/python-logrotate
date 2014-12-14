#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import subprocess
from Queue import Queue
import os
from datetime import date
import re
import gzip

__author__ = 'spooner'

def get_all_files_path():
    logs = []
    logs_dir = '/var/remote-log/'
    for path, dirs, files in os.walk(logs_dir):
        for f in files:
            if re.search(r'\.gz', f): continue
            log = path + '/' + f
            logs.append(log)
    return logs

def compress_logs(log):
    today = date.today()
    gziped_log = log + '.' + str(today) + '.gz'
    if os.path.exists(gziped_log):
        return 0 
    f_in = open(log, 'rb')
    f_out = gzip.open(gziped_log, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    return 0

def gziper(log, q):
    while True:
        log = q.get()
        print log
        compress_logs(log)
        q.task_done()

def main():
    queue = Queue()
    num_threads = 2
    logs = get_all_files_path()
    for log in logs:
        worker = Thread(target=gziper, args=(log, queue))
        worker.setDaemon(True)
        worker.start()

    for log in logs:
        queue.put(log)
    queue.join()


if __name__ == "__main__":
    main()