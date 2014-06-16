#!/usr/bin/python

from __future__ import print_function
from boto.cloudfront import CloudFrontConnection
import os, os.path, time

# change this for different distributions
AWS_CF_DISTRIBUTION_ID=""

todo_path="./to-be-processed"
done_path="./done"

if not os.path.exists(done_path):
    os.mkdir(done_path, 0755)
assert os.path.exists(done_path)
assert os.path.exists(todo_path)

def invalidate(paths):
    try:
        print("Invalidating...")
        conn = CloudFrontConnection()
        conn.create_invalidation_request(AWS_CF_DISTRIBUTION_ID, paths)
        return True
    except:
        return False

def completed(filepath):
    print("Completed file: ", filepath)
    os.rename(os.path.join(todo_path, filepath),
            os.path.join(done_path,filepath))

def process_all_files():
    files = os.listdir(todo_path)
    files.sort()
    for fn in files:
        fp = os.path.join(todo_path, fn)
        print("Processing file: ", fp)
        paths = map(str.rstrip, open(fp).readlines())
        if invalidate(paths):
            completed(fn)
        print("... (sleeping) ...")
        time.sleep(1200) # 20min

if __name__== "__main__":
    process_all_files()
