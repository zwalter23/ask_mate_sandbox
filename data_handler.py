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
def writer(cursor: RealDictCursor, data, file):
    keys = [key for key in data]
    print("DATACHECK : ", keys)
    cursor.execute(f"""INSERT INTO {file}
        VALUES ({data['id']},'{data['submission_time']}',{data['vote_number']},{data['question_id']},'{data['message']}','{data['image']}')
    """)

# def writer(data, file, x):
#     if file == "sample_data/question.csv":
#         fieldnames = fieldnames_q
#     else:
#         fieldnames = fieldnames_a
#     writer = csv.DictWriter(open(file, x), fieldnames=fieldnames)
#     if x == "w":
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#     else:
#         writer.writerow(data)

@connect_database.connection_handler
def reader(cursor: RealDictCursor, data):
    cursor.execute(f"SELECT * FROM {data}")
    return cursor.fetchall()
# def reader(csv_file):
#     reader = csv.DictReader(open(csv_file))
#     return reader


@connect_database.connection_handler
def edit(cursor:RealDictCursor, data, file):
    read = reader(file)
    cursor.execute(f"""UPDATE {file} 
        SET title = {data['title']}, message = {data['message']}
        WHERE id = {data['id']}
    """)
# def edit(data, file):
#     read = reader(file)
#     new = []
#     for row in read:
#         if data["id"] != row["id"]:
#             new.append(row)
#         else:
#             row.update(data)    #update the edited row/question
#             new.append(row)
#     writer(new, file, "w")


def delete_answer(answer_id):
    a_reader = reader("sample_data/answer.csv")
    new_a = []
    for row in a_reader:
        if answer_id == row["id"]:
            if row["image"]:
                if os.path.exists(f"static/img/answer/{row['image']}"):
                    os.remove(f"static/img/answer/{row['image']}")
        else:
            new_a.append(row)
    writer(new_a, "sample_data/answer.csv", "w")


def delete(id):
    q_reader = reader("sample_data/question.csv")
    a_reader = reader("sample_data/answer.csv")
    new_q = []
    new_a = []
    for row in q_reader:
        if id == row["id"]:
            if row["image"]:
                if os.path.exists(f"static/img/question/{row['image']}"):
                    os.remove(f"static/img/question/{row['image']}")    #delete the file(image)
        else:
            new_q.append(row)
    for row in a_reader:
        if id == row["question_id"]:
            if row["image"]:
                if os.path.exists(f"static/img/answer/{row['image']}"):
                    os.remove(f"static/img/answer/{row['image']}")
        else:
            new_a.append(row)
    writer(new_q, "sample_data/question.csv", "w")
    writer(new_a, "sample_data/answer.csv", "w")


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
