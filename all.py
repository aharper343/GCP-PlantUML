#!/usr/bin/env python3

import os.path
import subprocess
import re

EOL='\n'
PREFIX='!includeurl GCPPUML/'
#FIRSTLINE=PREFIX + 'common.puml' + EOL
FIRSTLINE=''
IGNORE_FILES=['all.puml', 'all_LARGE.puml', 'test.puml', 'common.puml']

def find_puml(path, ext='.puml'):
    path = os.path.abspath(path)
    lpath = len(path) + 1
    spriteExt = '-sprite' + ext
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname not in IGNORE_FILES:
                lfname = fname.lower()
                if lfname.endswith(ext) and not lfname.endswith(spriteExt):
                    yield os.path.join(root, fname)[lpath:]

def create(distDir):
    pumls = find_puml(distDir)
    allAlls={}
    for puml in pumls:
        tmp=puml.split('/')
        if len(tmp) == 1:
            allDir = ''
        else:
            allDir=tmp[0] + os.path.sep
        if '_LARGE' in puml:
            allFile='all_LARGE.puml'
        else:
            allFile='all.puml'
        if not allFile in allAlls:
            allAlls[allFile] = FIRSTLINE
        allAlls[allFile] = allAlls[allFile] + PREFIX + puml + EOL
        allFile = allDir + allFile
        if not allFile in allAlls:
            allAlls[allFile] = FIRSTLINE
        allAlls[allFile] = allAlls[allFile] + PREFIX + puml + EOL
    for k in allAlls:
        fpath=distDir + os.path.sep + k
        print('Writing:', fpath)
        with open(fpath,'w') as f:
            f.write(allAlls[k])

if __name__ == '__main__':
    distDir = os.path.abspath('dist')
    create(distDir)
