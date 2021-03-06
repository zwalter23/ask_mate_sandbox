import os
import re
import bcrypt
from psycopg2.extras import RealDictCursor
import connect_database

ALLOWED_EXTENSIONS = {'png', 'jpg'}


@connect_database.connection_handler
def writer(cursor: RealDictCursor, data, table):
    if table == 'question':
        cursor.execute(f"""
                            INSERT INTO question (submission_time, view_number, vote_number, title, message, image, email)
                            VALUES ('{data['submission_time']}', '{data['view_number']}', '{data['vote_number']}', '{data['title']}', '{data['message']}', '{data['image']}', '{data['email']}')
                        """)
    elif table == 'answer':
        cursor.execute(f"""
                            INSERT INTO answer (submission_time, vote_number, question_id, message, image, email)
                            VALUES('{data['submission_time']}', '{data['vote_number']}', '{data['question_id']}', '{data['message']}', '{data['image']}', '{data['email']}')
                        """)
    elif table == 'comment':
        cursor.execute(f"""
                            INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, email)
                            VALUES({data['question_id']}, {data['answer_id']}, '{data['message']}', '{data['submission_time']}',  '{data['edited_count']}', '{data['email']}')
                        """)


@connect_database.connection_handler
def tag(cursor: RealDictCursor, data):
    query = f"""INSERT INTO tag (name)
                       VALUES('{data}')"""
    cursor.execute(query)


@connect_database.connection_handler
def get_question_tags(cursor: RealDictCursor, question_id):
    query = f"""SELECT name,tag_id FROM tag FULL JOIN question_tag ON tag.id = question_tag.tag_id FULL JOIN question ON question_tag.question_id = question.id WHERE question.id='{question_id}'"""
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
def get_question(cursor: RealDictCursor, question_id):
    cursor.execute(f"SELECT * FROM question WHERE id = '{question_id}'")
    return cursor.fetchone()


@connect_database.connection_handler
def delete_tag(cursor: RealDictCursor, question_id):
    cursor.execute(f"DELETE FROM question_tag WHERE question_id='{question_id}'")


@connect_database.connection_handler
def delete_one_tag(cursor: RealDictCursor, question_id, tag_id):
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
def get_answer(cursor: RealDictCursor, message_id):
    cursor.execute(f"SELECT message FROM answer WHERE id = {message_id}")
    return cursor.fetchall()


@connect_database.connection_handler
def update(cursor: RealDictCursor, data, table):
    cursor.execute(f"""
                        UPDATE {table}
                        SET {f"title = '{data['title']}', " if data['title'] else ''} message = '{data['message']}' 
                        WHERE id = '{data['id']}'
                    """)


@connect_database.connection_handler
def view_count(cursor: RealDictCursor, question_id):
    cursor.execute(f"""UPDATE question 
                SET view_number = view_number + 1
                WHERE id = '{question_id}'
                    """)


@connect_database.connection_handler
def vote(cursor: RealDictCursor, column_id, table, modify):
    cursor.execute(f""" UPDATE {table}  
                        SET vote_number = vote_number {modify} 1
                        WHERE id = '{column_id}'
                    """)


@connect_database.connection_handler
def reputation(cursor: RealDictCursor, id, table, modify):
    cursor.execute(f"UPDATE users SET reputation = reputation {modify} 1 FROM {table} WHERE users.email={table}.email AND {table}.id = {id} ")


@connect_database.connection_handler
def counter_plus(cursor: RealDictCursor, id, table):
    cursor.execute(f"UPDATE users SET {table}_count = {table}_count + 1  FROM {table} WHERE users.email={table}.email  AND {table}.id = {reader(table)[0]['id']}")


@connect_database.connection_handler
def counter_minus(cursor: RealDictCursor, id, table):
    cursor.execute(f"UPDATE users SET {table}_count = {table}_count - 1  FROM {table} WHERE users.email={table}.email  AND {table}.id = {reader(table)[0]['id']}")



@connect_database.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
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
def delete(cursor: RealDictCursor, image_id):
    cursor.execute(f"SELECT image FROM question WHERE id = {image_id}")
    quest_img = cursor.fetchall()
    try:
        quest_img = [pic for pic in quest_img][0]['image']
        if os.path.exists(f"static/img/question/{quest_img}"):
            os.remove(f"static/img/question/{quest_img}")
    except:
        print("No image")
    cursor.execute(f"DELETE FROM comment WHERE question_id = {image_id}")
    cursor.execute(f"SELECT id FROM answer WHERE question_id = {image_id}")
    answer_id = cursor.fetchall()
    if answer_id:
        for i in range(len(answer_id)):
            ans_id = [num for num in answer_id][i]['id']
            delete_answer(ans_id)
    cursor.execute(f"DELETE FROM question  WHERE id = {image_id}")


@connect_database.connection_handler
def delete_comment(cursor: RealDictCursor, id):
    cursor.execute(f"DELETE FROM comment WHERE id = {id}")


@connect_database.connection_handler
def sort(cursor: RealDictCursor, x):
    order = re.split("=|&", x)[3]
    order_by = re.split("=|&", x)[1]
    cursor.execute(f"SELECT * FROM question ORDER BY {order_by} {order.upper()}")
    return cursor.fetchall()


@connect_database.connection_handler
def search_text(cursor: RealDictCursor, text):
    cursor.execute(f"SELECT * FROM question WHERE message LIKE '%{text}%' OR title LIKE '%{text}%'")
    questions = cursor.fetchall()
    cursor.execute(f"SELECT * FROM answer WHERE message LIKE '%{text}%'")
    answers = cursor.fetchall()
    return questions, answers


@connect_database.connection_handler
def new_user(cursor: RealDictCursor, email, password, registration_time):
    cursor.execute(f"""
                        INSERT INTO users (email, password_hash, registration_time, question_count, answer_count, comment_count, reputation )
                        VALUES ('{email}','{password}','{registration_time}','0','0','0','0')
                        """)


@connect_database.connection_handler
def get_users(cursor: RealDictCursor):
    cursor.execute(f"SELECT * FROM users;")
    users = cursor.fetchall()
    return users



def highlight(text, question, answer):
    for quest in question:
        if re.findall(text, quest['title']):
            titles = re.sub(text, f'<span style="font-weight:bold;background-color:#a71b1b;color:white">{text}</span>', quest['title'])
            title = quest["title"].replace(quest['title'], titles)
            quest.update({'title': title})
        if re.findall(text, quest['message']):
            message = re.sub(text, f'<span style="font-weight:bold;background-color:#a71b1b;color:white">{text}</span>', quest['message'])
            mess = quest["message"].replace(quest['message'], message)
            quest.update({'message': mess})

    for answ in answer:
        if re.findall(text, answ['message']):
            message = re.sub(text, f'<span style="font-weight:bold;background-color:#a71b1b;color:white">{text}</span>', answ['message'])
            mess = answ["message"].replace(answ['message'], message)
            answ.update({'message': mess})
    return question, answer


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')
#print(hash_password('qwe'))

def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

