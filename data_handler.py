import csv
import os
import re
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import random
import connect_database
#id,submission_time,view_number,vote_number,title,message,image
fieldnames_q = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
fieldnames_a = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
ALLOWED_EXTENSIONS = {'png', 'jpg'}


@connect_database.connection_handler
def writer(cursor: RealDictCursor, data, table):
    if table == 'question':
        query = f"""INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (data['id'], data['submission_time'], data['view_number'], data['vote_number'], data['title'],
                data['message'], data['image'])
    elif table == 'answer':
        query = f"""INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)
                       VALUES(%s, %s, %s, %s, %s, %s)"""
        values = (data['id'], data['submission_time'], data['vote_number'], data['question_id'], data['message'], data['image'])
    # elif table == 'comment':
    #     if data['question_id'] == 'NULL':
    #         query = f"""INSERT INTO comment
    #                        VALUES(DEFAULT, NULL, %s, %s, %s, %s)"""
    #         values = (data['answer_id'], data['message'], data['submission_time'],
    #                   data['edited_count'])
    #     else:
    #         query = f"""INSERT INTO comment
    #                        VALUES(DEFAULT, %s, NULL, %s, %s, %s)"""
    #         values = (data['question_id'], data['message'], data['submission_time'],
    #                   data['edited_count'])
    cursor.execute(query, values)


@connect_database.connection_handler
def reader(cursor: RealDictCursor, data):
    cursor.execute(f"SELECT * FROM {data}")
    return cursor.fetchall()


@connect_database.connection_handler
def edit_question(cursor:RealDictCursor, data):
    cursor.execute(f"""UPDATE question 
                SET title = %s, message = %s
                WHERE id = %s
    """, (data['title'], data['message'], data['id']))


@connect_database.connection_handler
def edit_answer(cursor:RealDictCursor, data):
    cursor.execute(f"""UPDATE question 
                SET message = '{data['message']}'
                WHERE id = '{data['id']}'
        """)
@connect_database.connection_handler
def edit(cursor:RealDictCursor, id, modify):
    if modify =="downvote":
        cursor.execute(f""" UPDATE question  
                            SET vote_number = vote_number - 1
                            WHERE id = '{id}'
                        """)
    elif modify == "upvote":
        cursor.execute(f""" UPDATE question  
                            SET vote_number = vote_number + 1
                            WHERE id = '{id}'
                        """)
    elif modify == "view_count":
        cursor.execute(f"""UPDATE question 
                SET view_number = view_number + 1
                WHERE id = '{id}'
                    """)

@connect_database.connection_handler
def delete_answer(cursor:RealDictCursor, answer_id):
    cursor.execute(f"SELECT image FROM answer WHERE id = {answer_id}")
    img = cursor.fetchall()
    img = [pic for pic in img][0]['image']
    if img:
        if os.path.exists(f"static/img/answer/{img}"):
            os.remove(f"static/img/answer/{img}")
    cursor.execute(f"DELETE FROM answer WHERE id = {answer_id}")


@connect_database.connection_handler
def delete(cursor:RealDictCursor, id):
    cursor.execute(f"SELECT image FROM question WHERE id = {id}")
    quest_img = cursor.fetchall()
    try:
        quest_img = [pic for pic in quest_img][0]['image']
        print("DATACHECK:",quest_img)
        if os.path.exists(f"static/img/question/{quest_img}"):
            os.remove(f"static/img/question/{quest_img}")
    except:
        print("No question image")


    cursor.execute(f"SELECT image FROM answer WHERE question_id = {id}")
    answer_img = cursor.fetchall()
    try:
        answer_img = [pic for pic in answer_img][0]['image']
        print("DATACHECK:", answer_img)
        if os.path.exists(f"static/img/answer/{answer_img}"):
            os.remove(f"static/img/answer/{answer_img}")
    except:
        print("No answer image")

    cursor.execute(f"DELETE FROM answer WHERE question_id = {id}")
    cursor.execute(f"DELETE FROM question  WHERE id = {id}")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def id_generator(file):
    id = 1
    read = reader(file)
    for row in read:
        if row:
            id = int(row["id"]) + 1
    return id


def sort(x):
    d = re.split("=|&", x)[3]
    y = re.split("=|&", x)[1]
    print("sorter:",x, d)
    questions = reader("question")
    questions = list(questions)
    try:
        lst = sorted(questions, key = lambda i: int(i[y]))
    except:
        lst = sorted(questions, key=lambda i: i[y].lower())
    if d == "down":
        lst = lst[::-1]
    for row in lst:
        print(row)
    return lst
