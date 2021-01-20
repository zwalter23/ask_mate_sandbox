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
        query = f"""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (data['submission_time'], data['view_number'], data['vote_number'], data['title'],
                data['message'], data['image'])
    elif table == 'answer':
        query = f"""INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                       VALUES(%s, %s, %s, %s, %s)"""
        values = (data['submission_time'], data['vote_number'], data['question_id'], data['message'], data['image'])
    elif table == 'comment':
        if data['question_id'] == 'NULL':
            query = f"""INSERT INTO comment
                           VALUES(NULL, %s, %s, %s, %s)"""
            values = (data['answer_id'], data['message'], data['submission_time'],
                      data['edited_count'])
        else:
            print(data)
            query = f"""INSERT INTO comment
                           VALUES(%s, NULL, %s, %s, %s)"""
            values = (data['question_id'], data['message'], data['submission_time'],
                      data['edited_count'])
    cursor.execute(query, values)


@connect_database.connection_handler
def reader(cursor: RealDictCursor, data):
    cursor.execute(f"SELECT * FROM {data} ORDER BY id DESC")
    return cursor.fetchall()


@connect_database.connection_handler
def edit_question(cursor:RealDictCursor, data):
    cursor.execute("""UPDATE question 
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
def edit_comment(cursor:RealDictCursor, data):
    cursor.execute(f"""UPDATE comment 
                    SET message = '{data['message']}'
                    WHERE id = '{data['id']}'
            """)


@connect_database.connection_handler
def view_count(cursor:RealDictCursor, id):
    cursor.execute(f"""UPDATE question 
                SET view_number = view_number + 1
                WHERE id = '{id}'
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
def edit_answer(cursor:RealDictCursor, id, modify):
    if modify =="downvote":
        cursor.execute(f""" UPDATE answer  
                            SET vote_number = vote_number - 1
                            WHERE id = '{id}'
                        """)
    elif modify == "upvote":
        cursor.execute(f""" UPDATE answer  
                            SET vote_number = vote_number + 1
                            WHERE id = '{id}'
                        """)


@connect_database.connection_handler
def delete_answer(cursor:RealDictCursor, answer_id):
    cursor.execute(f"SELECT image FROM answer WHERE id = {answer_id}")
    img = cursor.fetchall()
    try:
        img = [pic for pic in img][0]['image']
        if os.path.exists(f"static/img/answer/{img}"):
            os.remove(f"static/img/answer/{img}")
    except:
        print("No image")
    cursor.execute(f"DELETE FROM comment WHERE answer_id = {answer_id}")
    cursor.execute(f"DELETE FROM answer WHERE id = {answer_id}")


@connect_database.connection_handler
def delete(cursor:RealDictCursor, id):
    cursor.execute(f"SELECT image FROM question WHERE id = {id}")
    quest_img = cursor.fetchall()
    try:
        quest_img = [pic for pic in quest_img][0]['image']
        print("DATACHECK : ", quest_img)
        if os.path.exists(f"static/img/question/{quest_img}"):
            os.remove(f"static/img/question/{quest_img}")
    except:
        print("No image")
    cursor.execute("DELETE FROM comment WHERE question_id = %s", id)
    cursor.execute("SELECT id FROM answer WHERE question_id = %s", id)
    answer_id = cursor.fetchall()
    if answer_id:
        for i in range(len(answer_id)):
            answer_id = [num for num in answer_id][i]['id']
            print("DATACHECK: ", answer_id)
            cursor.execute("DELETE FROM comment WHERE answer_id = %s", answer_id)
    cursor.execute("DELETE FROM question  WHERE id = %s", id)


@connect_database.connection_handler
def delete_comment(cursor: RealDictCursor, id):
    cursor.execute("DELETE FROM comment WHERE id = %s", id)


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
