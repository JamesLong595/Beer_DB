# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:40:00 2020

@author: James Long
"""

import re

review_lst = list()
rec_cnt = 0
rev_err = 0
beer_err = 0

rbfh = open('ratebeer_db.txt')

for line in rbfh:
    if len(line) == 1:
        continue
    line = line.encode('ascii','replace').decode('ascii')
    if line.startswith('?'):
        line = line.translate(line.maketrans('', '', '?'))
    if line.startswith('beer/beerId'):
        try:
            beer_id = str(re.findall('^beer/beerId: (.+)', line)[0])
            continue
        except:
            beer_id = None
            beer_err = beer_err + 1
            continue
    elif line.startswith('review/profileName'):
        rec_cnt = rec_cnt + 1
        try:
            reviewer_lname = str(re.findall('^review/profileName: (.+)', line)[0])
            if (reviewer_lname, beer_id) not in review_lst:
                review_lst.append((reviewer_lname, beer_id))
            continue
        except:
            reviewer_lname = None
            rev_err = rev_err + 1
            continue

print()
print('unique reviews =',len(review_lst))
print('total records =',rec_cnt)
