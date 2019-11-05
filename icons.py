#!/usr/bin/env python3

import os.path
import subprocess
import re

REGULAR_SIZE='48x48'
LARGE_SIZE='256x256'
GCP='GCP-'

def convert(fromFile, toFile, scale):
    cmd = [ 'convert', '-resize', scale, fromFile, toFile]
    subprocess.check_call(cmd)

def cleanName(str):
    str = re.sub(r'\s', '-', str)
    str = re.sub(r'\&', 'And', str)
    return str

def resizeAndCopy(fromFile, toFile):
    if os.path.isfile(fromFile):
        convert(fromFile, toFile, REGULAR_SIZE)
        toFile=re.sub(r'\.png$', '_LARGE.png', toFile)
        convert(fromFile, toFile, LARGE_SIZE)
    else:
        print('ERROR:', fromFile, 'does not exist')

def process(fromFile, fileParts, toDir):
    if len(fileParts) == 2:
        fileParts[0] = cleanName(fileParts[0])
        fileParts[1] = cleanName(fileParts[1])
        toPath=toDir + os.path.sep + fileParts[0] + os.path.sep
        toFile='_'.join(fileParts)
        if not os.path.isdir(toPath):
            os.makedirs(toPath)
        resizeAndCopy(fromFile, toPath + toFile)
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
    extras = fromDir + os.path.sep + 'Extras' + os.path.sep
    for file in icons:
        lfile = file.lower()
        if extras in file or 'cloud tools' in lfile or 'eclipse' in lfile:
            print('Skipping:', file)
        else:
            fileParts = file.split('/')
            fileParts = fileParts[slice(fromDirCount, len(fileParts))]
            fileParts[1] = GCP + fileParts[1]
            process(file, fileParts, toDir)
    resizeAndCopy(extras + 'Google Cloud Platform.png', toDir + os.path.sep + GCP + 'Platform.png')
    for name in [ 'Kubernetes', 'Istio', 'TensorFlow']:
        resizeAndCopy(extras + 'Open Source Icons' + os.path.sep + name + '_logo.png', toDir + os.path.sep + GCP + name + '.png')

if __name__ == '__main__':
    copy('original.icons', 'icons')
