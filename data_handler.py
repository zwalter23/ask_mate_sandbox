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
            query = f"""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                           VALUES(NULL, %s, %s, %s, %s)"""
            values = (int(data['answer_id']), data['message'], data['submission_time'],
                      data['edited_count'])
        else:
            print(data)
            query = f"""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                           VALUES(%s, NULL, %s, %s, %s)"""
            values = (int(data['question_id']), data['message'], data['submission_time'],
                      data['edited_count'])
    cursor.execute(query, values)


@connect_database.connection_handler
def tag(cursor: RealDictCursor, data):
    query = f"""INSERT INTO tag (name)
                       VALUES('{data}')"""
    cursor.execute(query)


@connect_database.connection_handler
def get_question_tags(cursor: RealDictCursor, id):
    query = f"""SELECT name,tag_id FROM tag FULL JOIN question_tag ON tag.id = question_tag.tag_id FULL JOIN question ON question_tag.question_id = question.id WHERE question.id='{id}'"""
    cursor.execute(query)
    return cursor.fetchall()

@connect_database.connection_handler
def get_tag_id(cursor: RealDictCursor, tag):
    query = f"""SELECT id FROM tag WHERE name='{tag}'"""
    cursor.execute(query)
    return cursor.fetchone()

@connect_database.connection_handler
def reader(cursor: RealDictCursor, table):
    cursor.execute(f"SELECT * FROM {table} ORDER BY id DESC")
    return cursor.fetchall()

@connect_database.connection_handler
def get_question(cursor: RealDictCursor, id):
    cursor.execute(f"SELECT * FROM question WHERE id = '{id}'")
    return cursor.fetchone()

@connect_database.connection_handler
def delete_tag(cursor: RealDictCursor, question_id):
    cursor.execute(f"DELETE FROM question_tag WHERE question_id='{question_id}'")

@connect_database.connection_handler
def delete_one_tag(cursor: RealDictCursor, question_id,tag_id):
    cursor.execute(f"DELETE FROM question_tag WHERE question_id='{question_id}' AND tag_id='{tag_id}'")

@connect_database.connection_handler
def delete_tag_from_list(cursor: RealDictCursor, tag_id):
    cursor.execute(f"DELETE FROM question_tag WHERE tag_id='{tag_id}'")
    cursor.execute(f"DELETE FROM tag WHERE id='{tag_id}'")

@connect_database.connection_handler
def link_tag(cursor: RealDictCursor, question_id, tag_id):
    cursor.execute(f"""
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES ('{question_id}','{tag_id}')
                        ON CONFLICT DO NOTHING
                       """)

@connect_database.connection_handler
def update_tag(cursor: RealDictCursor, question_id, tag_id):
    cursor.execute(f"""
                        UPDATE question_tag
                        SET tag_id='{tag_id}'
                        WHERE question_id='{question_id}'""")



@connect_database.connection_handler
def get_answer(cursor:RealDictCursor, id):
    cursor.execute(f"SELECT message FROM answer WHERE id = {id}")
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
def update_answer(cursor:RealDictCursor, id, data):
    cursor.execute(f"UPDATE answer SET message = '{data}' WHERE id = {id}")


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
        if os.path.exists(f"static/img/question/{quest_img}"):
            os.remove(f"static/img/question/{quest_img}")
    except:
        print("No image")
    cursor.execute(f"DELETE FROM comment WHERE question_id = {id}")
    cursor.execute(f"SELECT id FROM answer WHERE question_id = {id}")
    answer_id = cursor.fetchall()
    if answer_id:
        for i in range(len(answer_id)):
            ans_id = [num for num in answer_id][i]['id']
            delete_answer(ans_id)
    cursor.execute(f"DELETE FROM question  WHERE id = {id}")


@connect_database.connection_handler
def delete_comment(cursor: RealDictCursor, id):
    cursor.execute(f"DELETE FROM comment WHERE id = {id}")


@connect_database.connection_handler
def sort(cursor: RealDictCursor, x):
    d = re.split("=|&", x)[3]
    y = re.split("=|&", x)[1]
    cursor.execute(f"SELECT * FROM question ORDER BY {y} {d.upper()}")
    return cursor.fetchall()


@connect_database.connection_handler
def search_text(cursor: RealDictCursor, text):
    cursor.execute(f"SELECT * FROM question WHERE message LIKE '%{text}%' OR title LIKE '%{text}%'")
    questions = cursor.fetchall()
    cursor.execute(f"SELECT * FROM answer WHERE message LIKE '%{text}%'")
    answers = cursor.fetchall()
    return questions, answers


def highlight(text, question, answer):
    for quest in question:
        if re.findall(text, quest['title']):
            titles = re.sub(text, f'<span style="font-weight:bold;background-color:#99ff66">{text}</span>', quest['title'])
            title = quest["title"].replace(quest['title'], titles)
            quest.update({'title': title})
        if re.findall(text, quest['message']):
            message = re.sub(text, f'<span style="font-weight:bold;background-color:#99ff66">{text}</span>', quest['message'])
            mess = quest["message"].replace(quest['message'], message)
            quest.update({'message': mess})

    for answ in answer:
        if re.findall(text, answ['message']):
            message = re.sub(text, f'<span style="font-weight:bold;background-color:#99ff66">{text}</span>', answ['message'])
            mess = answ["message"].replace(answ['message'], message)
            answ.update({'message': mess})
    return question, answer


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
