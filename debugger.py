# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:13:26 2020

@author: james
"""

#reviewer_id_tgt = 133
#beer_id_tgt = 605915

import re
#import cx_Oracle

#conn = cx_Oracle.connect("DB870", "<redacted>", "<redacted>")
#cur = conn.cursor()

#cur.execute('''
#            SELECT
#                reviewer_lname,
#                reviewer_id
#            FROM
#                reviewers
#            '''
#            )
#reviewer_lst = list(cur.fetchall())
#reviewer_dict = {}
#for tup in reviewer_lst:
#    reviewer_dict[tup[0]] = tup[1]
#del reviewer_lst
#del tup

review_lst = list()
rec_cnt = 0
rev_err = 0
beer_err = 0

#rbfh = open('ratebeer_sample.txt')    # test dataset
rbfh = open('ratebeer_db.txt')

for line in rbfh:
    if len(line) == 1:
        continue
    line = line.encode('ascii','replace').decode('ascii')
    if line.startswith('?'):
        line = line.translate(line.maketrans('', '', '?'))
#    if line.startswith('beer/name'):
#        try:
#            beer_name = str(re.findall('^beer/name: (.+)', line)[0])
#            continue
#        except:
#            beer_name = None
#            continue
    elif line.startswith('beer/beerId'):
        try:
            beer_id = str(re.findall('^beer/beerId: (.+)', line)[0])
            continue
        except:
            beer_id = None
            beer_err = beer_err + 1
            continue
#    elif line.startswith('beer/brewerId'):
#        try:
#            brewer_id = str(re.findall('^beer/brewerId: (.+)', line)[0])
#            continue
#        except:
#            brewer_id = None
#            continue
#    elif line.startswith('beer/ABV'):
#        try:
#            abv = str(re.findall('^beer/ABV: (.+)', line)[0])
#            continue
#        except:
#            abv = None
#            continue
#    elif line.startswith('beer/style'):
#        try:
#            style_name = str(re.findall('^beer/style: (.+)', line)[0])
#            continue
#        except:
#            style_name = None
#            continue
#    elif line.startswith('review/appearance'):
#        try:
#            appearance_rating = str(re.findall('^review/appearance: (.+)', line)[0])
#            appearance_rating = str(round((float(appearance_rating[0])/float(appearance_rating[2]))*100,0))
#            continue
#        except:
#            appearance_rating = None
#            continue
#    elif line.startswith('review/aroma') and len(line) == 19:
#        try:
#            aroma_rating = str(re.findall('^review/aroma: (.+)', line)[0])
#            aroma_rating = str(round((float(aroma_rating[0])/float(aroma_rating[2:]))*100,0))
#            continue
#        except:
#            aroma_rating = None
#            continue
#    elif line.startswith('review/aroma') and len(line) == 20:
#        try:
#            aroma_rating = str(re.findall('^review/aroma: (.+)', line)[0])
#            aroma_rating = str(round((float(aroma_rating[:2])/float(aroma_rating[3:]))*100,0))
#            continue
#        except:
#            aroma_rating = None
#            continue
#    elif line.startswith('review/palate'):
#        try:
#            palate_rating = str(re.findall('^review/palate: (.+)', line)[0])
#            palate_rating = str(round((float(palate_rating[0])/float(palate_rating[2]))*100,0))
#            continue
#        except:
#            palate_rating = None
#            continue
#    elif line.startswith('review/taste') and len(line) == 19:
#        try:
#            taste_rating = str(re.findall('^review/taste: (.+)', line)[0])
#            taste_rating = str(round((float(taste_rating[0])/float(taste_rating[2:]))*100,0))
#            continue
#        except:
#            taste_rating = None
#            continue
#    elif line.startswith('review/taste') and len(line) == 20:
#        try:
#            taste_rating = str(re.findall('^review/taste: (.+)', line)[0])
#            taste_rating = str(round((float(taste_rating[:2])/float(taste_rating[3:]))*100,0))
#            continue
#        except:
#            taste_rating = None
#            continue
#    elif line.startswith('review/overall') and len(line) == 21:
#        try:
#            overall_rating = str(re.findall('^review/overall: (.+)', line)[0])
#            overall_rating = str(round((float(overall_rating[0])/float(overall_rating[2:]))*100,0))
#            continue
#        except:
#            overall_rating = -1
#            continue
#    elif line.startswith('review/overall') and len(line) == 22:
#        try:
#            overall_rating = str(re.findall('^review/overall: (.+)', line)[0])
#            overall_rating = str(round((float(overall_rating[:2])/float(overall_rating[3:]))*100,0))
#            continue
#        except:
#            overall_rating = -1
#            continue
#    elif line.startswith('review/time'):
#        try:
#            comment_date = str(re.findall('^review/time: (.+)', line)[0])
#            continue
#        except:
#            comment_date = None
#            continue
    elif line.startswith('review/profileName'):
        try:
            reviewer_lname = str(re.findall('^review/profileName: (.+)', line)[0])
            continue
        except:
            reviewer_lname = None
            rev_err = rev_err + 1
            continue
#    elif line.startswith('review/text'):
#        try:
#            review_comment = str(re.findall('^review/text: (.+)', line)[0])
#        except:
#            review_comment = None
    if (reviewer_lname, beer_id) not in review_lst:
        review_lst.append((reviewer_lname, beer_id))
    rec_cnt = rec_cnt + 1

print()
print('unique reviews =',len(review_lst))
print('total records =',rec_cnt)

#    len(beer_name)
#    len(beer_id)
#    len(brewer_id)
#    len(overall_rating)
#    len(comment_date)
#    len(reviewer_lname)

#    reviewer_id = reviewer_dict.get(reviewer_lname,0)
#    if reviewer_id == reviewer_id_tgt and beer_id == beer_id_tgt:
#        break
