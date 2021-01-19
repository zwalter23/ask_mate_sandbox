from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import data_handler


app = Flask(__name__)
UPLOAD_FOLDER = 'static/img'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg'}


@app.route("/list")
@app.route("/")
def list():
        question = data_handler.reader("question")
        quest = []
        a = [x for x in question]
        for row in a[::-1]:
            quest.append(row)
        return render_template("list.html", questions=quest)


@app.route("/visitor/<question_id>")
def visitor(question_id):
    question = data_handler.reader("question")
    for row in question:
        if question_id == row["id"]:
            row["view_number"] = int(row["view_number"]) + 1
            data_handler.edit(row, "question")
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>", methods=["GET", "POST"])
def quest(question_id):
    question = data_handler.reader("question")
    answer = data_handler.reader("answer")
    print(question_id, [x['id'] for x in question])
    return render_template("question.html", question = question, answer = answer, id = int(question_id))


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    questions = data_handler.reader("question")
    for row in questions:
        if row["id"] == int(question_id):
            return render_template("new_answer.html", question=row, id=question_id)


@app.route("/save_answer/<question_id>", methods=["GET", "POST"])
def save_answer(question_id):
    if request.method == "POST":
        id = data_handler.id_generator("answer")
        answer = request.form["answer"]
        f = request.files["file"]
        if f:
            f.filename = "id"+str(id)+f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], "answer", f.filename))
        new_answer = {"id": id, "submission_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "vote_number": 0,
                      "question_id": question_id, "message": answer, "image": f.filename}
        data_handler.writer(new_answer, "answer")
    return redirect(f"/question/{question_id}")


@app.route("/save", methods=["GET", "POST"])
def save():
    if request.method == "POST":
        id = data_handler.id_generator("question")
        title = request.form["title"]
        message = request.form["message"]
        f = request.files["file"]
        if f:
            f.filename = "id"+str(id)+f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],"question", f.filename))
        question = {"id": id, "submission_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "view_number": 0,
                    "vote_number": 0, "title": title, "message": message, "image": f.filename}
        data_handler.writer(question, "question", "a")
    return redirect(f"/question/{id}")


@app.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    return render_template("file_upload.html")


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    question = data_handler.reader("question")
    return  render_template("edit.html", question = question, id = question_id)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_quest(id):
    title = request.form["title"]
    message = request.form["message"]
    question = {"id": id, "title": title, "message": message}
    data_handler.edit(question, "question")
    return redirect(f"/question/{id}")


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    data_handler.delete(question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["GET", "POST"])
def delete_answer(answer_id, question_id):
    data_handler.delete_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote_down", methods=["GET", "POST"])
def vote_down(question_id):
    question = data_handler.reader("question")
    for row in question:
        if row["id"] == question_id:
            if int(row["vote_number"]) > 0:
                row["vote_number"] = int(row["vote_number"]) - 1
                data_handler.edit(row, "question")
    return redirect("/sort?sort=vote_number&dir=down")


@app.route("/question/<question_id>/vote_up", methods=["GET", "POST"])
def vote_up(question_id):
    question = data_handler.reader("question")
    for row in question:
        if row["id"] == question_id:
            row["vote_number"] = int(row["vote_number"]) + 1
            data_handler.edit(row, "question")
    return redirect("/sort?sort=vote_number&dir=down")


@app.route("/answer/<answer_id>/vote_down/<question_id>", methods=["GET", "POST"])
def answer_vote_down(answer_id, question_id):
    answer = data_handler.reader("answer")
    for row in answer:
        if row["id"] == answer_id:
            if int(row["vote_number"]) > 0:
                row["vote_number"] = int(row["vote_number"]) - 1
                data_handler.edit(row, "answer")
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote_up/<question_id>", methods=["GET", "POST"])
def answer_vote_up(answer_id, question_id):
    answer = data_handler.reader("answer")
    for row in answer:
        if row["id"] == answer_id:
            row["vote_number"] = int(row["vote_number"]) + 1
            data_handler.edit(row, "answer")
    return redirect(f"/question/{question_id}")


@app.route("/sort", methods=["GET", "POST"])
def sort():
     sorting = request.query_string
     sorting = sorting.decode()
     # x = request.form["sort"]  # if select sort
     sorted = data_handler.sort(sorting)
     return render_template("list.html", questions=sorted)


if __name__ == "__main__":
    app.run(debug=True)
