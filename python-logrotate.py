#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import os
import re
import gzip
from datetime import date


def get_all_files_path():
    logs = []
    logs_dir = '/tmp/log/'
    for path, dirs, files in os.walk(logs_dir):
        for f in files:
            if re.search(r'\.gz', f): continue
            log = path + '/' + f
            logs.append(log)
    # разобрать list на 32 части
    return logs

def compress_logs(log):
    print log
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


def main():
    pool = Pool(processes=32)
    logs = get_all_files_path()
    result = pool.apply_async(compress_logs, ['/tmp/log/log-1/vos-service.log.shell'])
    print result.get(timeout=1)
    print pool.map(compress_logs, logs)

if __name__ == "__main__":
    main()
