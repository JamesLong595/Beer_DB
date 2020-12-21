# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 22:40:00 2020

@author: James Long
"""

import cx_Oracle
import re

# Connect as user "DB870" with password "<redacted>" to the "CDB9" service
# running on "<redacted>".
conn = cx_Oracle.connect("DB870", "<redacted>", "<redacted>")
cur = conn.cursor()

#rbfh = open('ratebeer_sample.txt')    # test dataset, first 5 records
rbfh = open('ratebeer_db.txt')    # full dataset
#rbfh = open('ratebeer_db_trimmed.txt')    # partial dataset to speed disconnect recovery

# if a restart is needed due to disconnect before the script completes, you can
# comment the following lines down to (but not including) the error logging block
cur.execute('''
            SELECT
                beer_id
            FROM
                beers
            '''
            )
beer_id_lst = list(cur.fetchall())
cur.execute('''
            SELECT
                brewer_id,
                beer_name
            FROM
                beers
            '''
            )
beer_unq_lst = list(cur.fetchall())

cur.execute('''
            SELECT
                style_name,
                style_id
            FROM
                styles
            '''
            )
style_lst = list(cur.fetchall())
style_dict = {}
for tup in style_lst:
    style_dict[tup[0]] = tup[1]
cur.execute('''
            SELECT
                style_id
            FROM
                styles
            '''
            )
style_lst = list(cur.fetchall())
new_style_id = int(max(style_lst)[0])
del style_lst

cur.execute('''
            SELECT
                reviewer_lname,
                reviewer_id
            FROM
                reviewers
            '''
            )
reviewer_lst = list(cur.fetchall())
reviewer_dict = {}
for tup in reviewer_lst:
    reviewer_dict[tup[0]] = tup[1]
del reviewer_lst

cur.execute('''
            SELECT
                brewer_id
            FROM
                brewers
            '''
            )
brewer_lst = list(cur.fetchall())

cur.execute('''
            SELECT
                reviewer_id,
                beer_id,
                comment_date
            FROM
                comments
            '''
            )
comment_lst = list(cur.fetchall())

cur.execute('''
            SELECT
                reviewer_id,
                beer_id
            FROM
                beer_reviews
            '''
            )
beer_review_lst = list(cur.fetchall())

# error logging
reviewer_err_lst = list()
reviewer_err_cnt = 0
brewer_err_lst = list()
brewer_err_cnt = 0
style_err_lst = list()
style_err_cnt = 0
beer_err_lst = list()
beer_err_cnt = 0
beer_review_err_lst = list()
beer_review_err_cnt = 0
comment_err_lst = list()
comment_err_cnt = 0

print()
print('******* BEGIN *******')
print()

for line in rbfh:
    if len(line) == 1:
        continue
    line = line.encode('ascii','replace').decode('ascii')
    if line.startswith('?'):
        line = line.translate(line.maketrans('', '', '?'))
    if line.startswith('beer/name'):
        try:
            beer_name = str(re.findall('^beer/name: (.+)', line)[0])
            continue
        except:
            beer_name = 0
            continue
    elif line.startswith('beer/beerId'):
        try:
            beer_id = int(re.findall('^beer/beerId: (.+)', line)[0])
            continue
        except:
            beer_id = 0
            continue
    elif line.startswith('beer/brewerId'):
        try:
            brewer_id = int(re.findall('^beer/brewerId: (.+)', line)[0])
            continue
        except:
            brewer_id = -1
            continue
    elif line.startswith('beer/ABV'):
        try:
            abv = float(re.findall('^beer/ABV: (.+)', line)[0])
            continue
        except:
            abv = 0
            continue
    elif line.startswith('beer/style'):
        try:
            style_name = str(re.findall('^beer/style: (.+)', line)[0])
            continue
        except:
            style_name = 'unknown'
            continue
    elif line.startswith('review/appearance'):
        try:
            appearance_rating = str(re.findall('^review/appearance: (.+)', line)[0])
            appearance_rating = str(round((float(appearance_rating[0])/float(appearance_rating[2]))*100,0))
            continue
        except:
            appearance_rating = None
            continue
    elif line.startswith('review/aroma') and len(line) == 19:
        try:
            aroma_rating = str(re.findall('^review/aroma: (.+)', line)[0])
            aroma_rating = str(round((float(aroma_rating[0])/float(aroma_rating[2:]))*100,0))
            continue
        except:
            aroma_rating = None
            continue
    elif line.startswith('review/aroma') and len(line) == 20:
        try:
            aroma_rating = str(re.findall('^review/aroma: (.+)', line)[0])
            aroma_rating = str(round((float(aroma_rating[:2])/float(aroma_rating[3:]))*100,0))
            continue
        except:
            aroma_rating = None
            continue
    elif line.startswith('review/palate'):
        try:
            palate_rating = str(re.findall('^review/palate: (.+)', line)[0])
            palate_rating = str(round((float(palate_rating[0])/float(palate_rating[2]))*100,0))
            continue
        except:
            palate_rating = None
            continue
    elif line.startswith('review/taste') and len(line) == 19:
        try:
            taste_rating = str(re.findall('^review/taste: (.+)', line)[0])
            taste_rating = str(round((float(taste_rating[0])/float(taste_rating[2:]))*100,0))
            continue
        except:
            taste_rating = None
            continue
    elif line.startswith('review/taste') and len(line) == 20:
        try:
            taste_rating = str(re.findall('^review/taste: (.+)', line)[0])
            taste_rating = str(round((float(taste_rating[:2])/float(taste_rating[3:]))*100,0))
            continue
        except:
            taste_rating = None
            continue
    elif line.startswith('review/overall') and len(line) == 21:
        try:
            overall_rating = str(re.findall('^review/overall: (.+)', line)[0])
            overall_rating = str(round((float(overall_rating[0])/float(overall_rating[2:]))*100,0))
            continue
        except:
            overall_rating = -1
            continue
    elif line.startswith('review/overall') and len(line) == 22:
        try:
            overall_rating = str(re.findall('^review/overall: (.+)', line)[0])
            overall_rating = str(round((float(overall_rating[:2])/float(overall_rating[3:]))*100,0))
            continue
        except:
            overall_rating = -1
            continue
    elif line.startswith('review/time'):
        try:
            comment_date = int(re.findall('^review/time: (.+)', line)[0])
            continue
        except:
            comment_date = -1
            continue
    elif line.startswith('review/profileName'):
        try:
            reviewer_lname = str(re.findall('^review/profileName: (.+)', line)[0])
            continue
        except:
            reviewer_lname = 0
            continue
    elif line.startswith('review/text'):
        try:
            review_comment = str(re.findall('^review/text: (.+)', line)[0])
        except:
            review_comment = None

    if reviewer_lname != 0:
        reviewer_id = reviewer_dict.get(reviewer_lname,0)
        if reviewer_id == 0:
            try:
                cur.execute('''
                            INSERT INTO
                                reviewers(reviewer_lname)
                            VALUES
                                (:reviewer_lname)
                            ''',
                            [reviewer_lname]
                            )
                conn.commit();
                cur.execute('''
                            SELECT
                                reviewer_id
                            FROM
                                reviewers
                            WHERE
                                reviewer_lname = :reviewer_lname
                            ''',
                            [reviewer_lname]
                            )
                reviewer_dict[reviewer_lname] = cur.fetchone()[0]
                reviewer_id = reviewer_dict.get(reviewer_lname)
            except Exception as nam_err:
                reviewer_err_lst.append(reviewer_lname)
                reviewer_err_cnt = reviewer_err_cnt + 1
                print('reviewer error',reviewer_err_cnt)
                print(nam_err)

    if (brewer_id,) not in brewer_lst:
        try:
            cur.execute('''
                        INSERT INTO
                            brewers(brewer_id)
                        VALUES
                            (:brewer_id)
                        ''',
                        [brewer_id]
                        )
            conn.commit();
            brewer_lst.append((brewer_id,))
        except Exception as brew_err:
            brewer_err_lst.append(brewer_id)
            brewer_err_cnt = brewer_err_cnt + 1
            print('brewer error',brewer_err_cnt)
            print(brew_err)

    style_id = style_dict.get(style_name,0)
    if style_id == 0:
        new_style_id = new_style_id + 1
        style_id = new_style_id
        try:
            cur.execute('''
                        INSERT INTO
                            styles(style_id,category_id,style_name)
                        VALUES
                            (:style_id,-1,:style_name)
                        ''',
                        [style_id, style_name]
                        )
            conn.commit();
            style_dict[style_name] = style_id
        except Exception as sty_err:
            style_err_lst.append(style_id)
            style_err_cnt = style_err_cnt + 1
            print('style error',style_err_cnt)
            print(sty_err)

    if beer_name == 0:
        continue
    if beer_id == 0:
        continue
    if (brewer_id, beer_name) in beer_unq_lst:
        continue
    if (beer_id,) not in beer_id_lst:
        try:
            cur.execute('''
                        INSERT INTO
                            beers(beer_id, brewer_id, beer_name, style_id, abv, ibu, srm)
                        VALUES
                            (:beer_id, :brewer_id, :beer_name, :style_id, :abv, 0, -1)
                        ''',
                        [beer_id, brewer_id, beer_name, style_id, abv]
                        )
            conn.commit();
            beer_id_lst.append((beer_id,))
        except Exception as beer_err:
            beer_err_lst.append(beer_id)
            beer_err_cnt = beer_err_cnt + 1
            print('beer error',beer_err_cnt)
            print(beer_err)

    if reviewer_lname == 0:
        continue
    if overall_rating == -1:
        continue
    if (reviewer_id, beer_id) not in beer_review_lst:
        try:
            cur.execute('''
                        INSERT INTO
                            beer_reviews(reviewer_id, beer_id, overall_rating, appearance_rating, aroma_rating, palate_rating, taste_rating)
                        VALUES
                            (:reviewer_id, :beer_id, :overall_rating, :appearance_rating, :aroma_rating, :palate_rating, :taste_rating)
                        ''',
                        [reviewer_id, beer_id, overall_rating, appearance_rating, aroma_rating, palate_rating, taste_rating]
                        )
            conn.commit();
            beer_review_lst.append((reviewer_id, beer_id))
        except Exception as rev_err:
            beer_review_err_lst.append((reviewer_id, beer_id))
            beer_review_err_cnt = beer_review_err_cnt + 1
            print('beer review error',beer_review_err_cnt)
            print(rev_err)

    if comment_date == -1:
        continue
    if (reviewer_id, beer_id, comment_date) not in comment_lst:
        try:
            len(review_comment)
            try:
                cur.execute('''
                            INSERT INTO
                                comments(reviewer_id, beer_id, comment_date, review_comment)
                            VALUES
                                (:reviewer_id, :beer_id, :comment_date, :review_comment)
                            ''',
                            [reviewer_id, beer_id, comment_date, review_comment]
                            )
                conn.commit();
                comment_lst.append((reviewer_id, beer_id, comment_date))
            except Exception as com_err:
                comment_err_lst.append((reviewer_id, beer_id, comment_date))
                comment_err_cnt = comment_err_cnt + 1
                print('comment error',comment_err_cnt)
                print(com_err)
        except:
            continue

conn.commit()
cur.close()
