<<<<<<< HEAD
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
=======
from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import data_handler


app = Flask(__name__)
UPLOAD_FOLDER = 'static/img'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg'}


@app.route("/list")
def list_default():
    question = data_handler.reader("question")
    return render_template("list.html", questions=question)


@app.route("/")
def list_last_5():
    question = data_handler.reader("question")[:5]
    return render_template("list.html", questions=question)


@app.route("/search")
def search():
    text = request.query_string.decode().split("=")[1]
    questions, answers = data_handler.search_text(text)
    questions, answers = data_handler.highlight(text, questions, answers)
    return render_template("search.html", questions=questions, answers=answers, text=text)


@app.route("/visitor/<question_id>")
def visitor(question_id):
    data_handler.view_count(question_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>", methods=["GET", "POST"])
def quest(question_id):
    tags = data_handler.get_question_tags(question_id)
    question = data_handler.reader("question")
    answer = data_handler.reader("answer")
    comment = data_handler.reader("comment")
    return render_template("question.html", question=question, answer=answer, comment=comment, tags=tags, id=int(question_id))


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    questions = data_handler.reader("question")
    for row in questions:
        if row["id"] == int(question_id):
            return render_template("new_answer.html", question=row, id=int(question_id))


@app.route("/save_answer/<question_id>", methods=["GET", "POST"])
def save_answer(question_id):
    if request.method == "POST":
        answer = request.form["answer"]
        f = request.files["file"]
        if f:
            f.filename = "id"+str(id)+f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], "answer", f.filename))
        new_answer = {"submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "vote_number": 0,
                      "question_id": question_id, "message": answer, "image": f.filename}
        data_handler.writer(new_answer, "answer")
    return redirect(f"/question/{question_id}")


@app.route("/save", methods=["GET", "POST"])
def save():
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        f = request.files["file"]
        if f:
            f.filename = "id"+str(id)+f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], "question", f.filename))
        question = {"submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "view_number": 0,
                    "vote_number": 0, "title": title, "message": message, "image": f.filename}
        data_handler.writer(question, "question")
    return redirect(f"/question/{data_handler.reader('question')[0]['id']}")


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    question = data_handler.reader("question")
    return render_template("edit.html", question=question, id=int(question_id))


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_quest(id):
    title = request.form["title"]
    message = request.form["message"]
    question = {"id": id, "title": title, "message": message}
    data_handler.update(question, "question")
    return redirect(f"/question/{id}")


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    data_handler.delete(question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/edit/<question_id>", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if request.method == "POST":
        data = {"id": answer_id, "message": request.form.get("text")}
        data_handler.update(data, "answer")
        print("DATACHECK:", question_id)
        return redirect(f"/question/{question_id}")
    answer = data_handler.get_answer(answer_id)[0]['message']
    return render_template("edit_answer.html", answer=answer, answer_id=int(answer_id), question_id=int(question_id))


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["GET", "POST"])
def delete_answer(answer_id, question_id):
    data_handler.delete_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote_down", methods=["GET", "POST"])
def vote_down(question_id):
    data_handler.vote(question_id, "question", "-")
    return redirect("/list")


@app.route("/question/<question_id>/vote_up", methods=["GET", "POST"])
def vote_up(question_id):
    data_handler.vote(question_id, "question", "+")
    return redirect("/list")


@app.route("/answer/<answer_id>/vote_down/<question_id>", methods=["GET", "POST"])
def answer_vote_down(answer_id, question_id):
    data_handler.vote(answer_id, "answer", "-")
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote_up/<question_id>", methods=["GET", "POST"])
def answer_vote_up(answer_id, question_id):
    data_handler.vote(answer_id, "answer", "+")
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag_to_question(question_id):
    if request.method == "POST":
        tag_id = data_handler.get_tag_id(request.form['tags'])['id']
        data_handler.link_tag(question_id, tag_id)
        return redirect(f"/question/{question_id}")
    question = data_handler.get_question(question_id)
    question_tag = data_handler.get_question_tags(question_id)
    tags = data_handler.reader("tag")
    return render_template("new_tag.html", tags=tags, id=question_id, question=question, question_tag=question_tag)


@app.route("/delete-tag/<question_id>")
def delete_tag(question_id):
    data_handler.delete_tag(question_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete-tag", methods=["POST", "GET"])
def delete_tag_from_list(question_id):
    if request.method == "POST":
        tag_id = data_handler.get_tag_id(request.form['tags'])['id']
        data_handler.delete_tag_from_list(tag_id)
        return redirect(f"/question/{question_id}/new-tag")


@app.route("/question/<id>/add-new-tag", methods=["GET", "POST"])
def add_new_tag(id):
    new_tag = request.form['new_tag']
    data_handler.tag(new_tag)
    return redirect(f"/question/{id}/new-tag")


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_one_tag(question_id, tag_id):
    data_handler.delete_one_tag(question_id, tag_id)
    return redirect(f"/question/{question_id}")


@app.route("/sort", methods=["GET", "POST"])
def sort():
    sorting = data_handler.sort(request.query_string.decode())
    return render_template("list.html", questions=sorting)


@app.route("/comment/<question_id>/add", methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        comment = request.form.get('comment')
        data = {"question_id": question_id, "answer_id": 'NULL', "message": comment,
                "submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "edited_count": 0}
        data_handler.writer(data, "comment")
        return redirect(f"/question/{question_id}")
    return render_template("add_comment.html", id=int(question_id))


@app.route("/comment/<answer_id>/add/<question_id>", methods=["GET", "POST"])
def add_answer_comment(answer_id, question_id):
    if request.method == "POST":
        comment = request.form.get('comment')
        data = {"question_id": 'NULL', "answer_id": answer_id, "message": comment,
                "submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "edited_count": 0}
        data_handler.writer(data, "comment")
        return redirect(f"/question/{question_id}")
    return render_template("add_answer_comment.html", question_id=question_id, answer_id=answer_id)


@app.route("/comment/<comment_id>/delete/<question_id>")
def delete_comment(comment_id, question_id):
    data_handler.delete_comment(comment_id)
    return redirect(f"/question/{question_id}")


@app.route("/comment/<comment_id>/edit/<question_id>", methods=["GET", "POST"])
def edit_comment(comment_id, question_id):
    if request.method == "POST":
        data = {"id": comment_id, "message": request.form.get("comment")}
        data_handler.update(data, "comment")
        return redirect(f"/question/{question_id}")
    comment = data_handler.reader("comment")
    return render_template("edit_comment.html", comment=comment, comment_id=int(comment_id), question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> sprint2/development
