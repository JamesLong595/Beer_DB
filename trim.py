# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:12:20 2020

@author: james
"""

oldfh = open('ratebeer_db.txt')

newfh = open('ratebeer_db_trimmed.txt', mode='w')

linecnt = 0

for line in oldfh:
    linecnt = linecnt + 1
    if linecnt <= 39200000:
        continue
    else:
        newfh.write(line)

newfh.close()
