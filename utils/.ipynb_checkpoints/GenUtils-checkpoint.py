#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Sep 28 18:45:02 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os

def question(question, answers):
    answ = None
    while answ not in answers:
        print('Please enter only: ')
        print(*answers, sep=', ')
        
        answ = input(question+'Answer: ')
    return(answ)

def make_folder(path, name):
    if name is None:
        folder = path
    else:
        folder = path+'/'+name
    if os.path.exists(folder):
        pass
    else:        
        os.mkdir(folder)
        
    return(folder)

def get_paths(PATH, ixt):
    import re
    import fnmatch
    os.chdir(PATH)
    ext='*.'+ixt
    chkCase = re.compile(fnmatch.translate(ext), re.IGNORECASE)
    files = [f for f in os.listdir(PATH) if chkCase.match(f)]
    return(files)