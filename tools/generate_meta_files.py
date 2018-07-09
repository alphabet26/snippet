#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# 没错，我是中文注释

import os, sys 
import filecmp 
import re 
import string
from distutils import dir_util 
import shutil 
import zipfile
import json 
import io
import datetime
import subprocess
import hashlib
from pprint import pprint
from inspect import getsourcefile
from os.path import abspath

def copyfile(src, dst):
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), ""):
            os.write(fout, x)
    finally:
        try: os.close(fin)
        except: pass
        try: os.close(fout)
        except: pass

def generate_meta_files(dir):
    file_list_map = {}
    for dirName, subdirList, fileList in os.walk(dir):
            abs_path = os.path.abspath(dirName)
            # print "abs_path:%s" % abs_path
            # print "subdirList:%s" % subdirList
            # print "fileList:%s" % fileList
            for f in fileList:                       # 
                full_path = os.path.join(abs_path, f)
                md5_val   = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
                rel_path  = os.path.join(os.path.relpath(abs_path, dir), f)
                file_list_map[rel_path] = md5_val

    # for key1 in file_list_map:
    #     md5_val1 = file_list_map[key1]
    #     for key2 in file_list_map:
    #         md5_val2 = file_list_map[key2]
    #         if md5_val1 == md5_val2 and key1!=key2:
    #             print("!!key1:%s key2:%s is the same files" % (key1, key2))
    
    # copy files to meta
    meta_dir = os.path.join(os.path.join(dir, ".."), "meta")
    for key in file_list_map:
        meta_file_path = os.path.join(meta_dir, file_list_map[key])
        full_path = os.path.join(dir, key)
        print("coppy %s to %s" % (full_path, meta_file_path))
        shutil.copyfile(full_path, meta_file_path)


    output_file = os.path.join(os.path.join(dir, ".."), "files.meta")
    print("output_file:%s" % output_file)
    # 写入文件
    with io.open(output_file,'w',encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(file_list_map, ensure_ascii=False)))

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--path",                       # 指定文件目录
                  dest="path", 
                  help="specify the path")
    (options, args) = parser.parse_args(sys.argv[1:])
    print("sys.argv[1:]:%s" % sys.argv[1:])
    print("args.path:%s" % options.path)

    # check the arguments
    if options.path == None: 
        print("ERROR! path is None!")
        return

    options.path = os.path.abspath(options.path)              # to absolute path
    generate_meta_files(options.path)

if __name__ == '__main__': 
    main()