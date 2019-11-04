#!/usr/bin/env python3

import os.path
import subprocess
import re


def convert(fromFile, toFile, scale):
    cmd = [ 'convert', '-resize', scale, fromFile, toFile]
    subprocess.check_call(cmd)

def cleanName(str):
    str = re.sub(r'\s', '', str)
    str = re.sub(r'\&', 'And', str)
    return str

def process(fromFile, fileParts, toDir):
    if len(fileParts) == 2:
        fileParts[0] = cleanName(fileParts[0])
        fileParts[1] = cleanName(fileParts[1])
        toPath=toDir + os.path.sep + fileParts[0] + os.path.sep
        toFile='_'.join(fileParts)
        if not os.path.isdir(toPath):
            os.makedirs(toPath)
        convert(fromFile, toPath + toFile, '32x32')
        toFile=re.sub(r'\.png$', '_LARGE.png', toFile)
        convert(fromFile, toPath + toFile, '128x128')
    else:
        print('Skipping:', fromFile)

def find_images(path, ext='.png'):
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.lower().endswith(ext):
                yield os.path.join(root, fname)

def copy(fromDir, toDir):
    fromDir = os.path.abspath(fromDir)
    fromDirCount = len(fromDir.split('/'))
    toDir = os.path.abspath(toDir)
    icons = find_images(fromDir)
    extras = os.path.sep + 'extras' + os.path.sep
    for file in icons:
        lfile = file.lower()
        if extras in lfile or 'cloud tools' in lfile or 'eclipse' in lfile:
            print('Skipping:', file)
        else:
            fileParts = file.split('/')
            fileParts = fileParts[slice(fromDirCount, len(fileParts))]
            process(file, fileParts, toDir)

if __name__ == '__main__':
    copy('original.icons', 'icons')
