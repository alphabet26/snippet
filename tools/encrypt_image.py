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
from pprint import pprint
from inspect import getsourcefile
from os.path import abspath


def encrypt_image(res_dir, operation):   
    print("encrypt_image res_dir:%s operation:%s" % (res_dir, operation) )
    # find .png AND .jpg
    for root, dirs, files in os.walk(res_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                img_path = os.path.join(root, file)       # img path
                #print(img_path)
                in_file = open(img_path, "rb") # opening for [r]eading as [b]inary
                data = in_file.read(1) # if you only wanted to read 512 bytes, do .read(512)
                in_file.close()

                try:
                    
                    #data[0] ^= 10
                    byte = ord(data[0])

                    bNeedOpera = False;
                    if operation=="encrypt" and byte!=131 and byte!=245:
                        bNeedOpera = True
                    if operation=="decrypt" and (byte==131 or byte==245):
                        bNeedOpera = True

                    #print(byte)
                    if bNeedOpera==True:
                        # print("%s %s" % (operation, img_path))
                        num_val = byte ^ 10
                        chr_val = chr(num_val)
                        out_file = open(img_path, "r+b") # open for [w]riting as [b]inary
                        out_file.seek(0)
                        out_file.write(chr_val)
                        out_file.close()
                except Exception:
                    print("ERROR!write image fail:%s" % img_path)


def main(): 

    if len(sys.argv)!=2 :
        print("ERROR!WRONG NUMBER OF ARGV!")
        return

    #print ("argv:%s" % sys.argv[1])
    work_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
    print "work_path:%s" % work_path

        
    res_dir = os.path.join(os.path.join(work_path, os.pardir), "res")   # 

    encrypt_image(res_dir, sys.argv[1])

if __name__ == '__main__': 
    main()