#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:16:09 2021

@author: alok
"""

def shorthand(name):
    short = [x[0] for x in name.split()]
    return "".join(short)