from flask import Flask, render_template, request, jsonify, redirect
from chatbot import get_response
from database import (
    init_db,
    save_chat,
    get_chats,
    clear_chats,
    get_chat_count,
    get_unanswered_questions,
    add_faq,
    add_order
)
app = Flask(__name__)

init_db()


@app.route("/")
def home():
    chats = get_chats()

    return render_template(
        "index.html",
        chats=chats
    )


@app.route("/chat", methods=["POST"])
def chat():

    message = request.json["message"]

    response = get_response(message)

    save_chat(
        message,
        response
    )

    return jsonify({
        "response": response
    })


@app.route("/history")
def history():

    chats = get_chats()

    return render_template(
        "history.html",
        chats=chats
    )


@app.route("/clear")
def clear():

    clear_chats()

    return redirect("/")
@app.route("/admin")
def admin():

    chats = get_chats()

    count = get_chat_count()

    unanswered = get_unanswered_questions()

    return render_template(
        "admin.html",
        chats=chats,
        count=count,
        unanswered=unanswered
    )


@app.route("/search")
def search():

    keyword = request.args.get(
        "keyword",
        ""
    )

    chats = get_chats()

    filtered = []

    for chat in chats:

        if (
            keyword.lower() in chat[0].lower()
            or keyword.lower() in chat[1].lower()
        ):
            filtered.append(chat)

    return render_template(
        "admin.html",
        chats=filtered,
        count=len(filtered),
        unanswered=get_unanswered_questions()
    )


@app.route("/add_faq", methods=["POST"])
def add_faq_route():

    question = request.form["question"]

    answer = request.form["answer"]

    add_faq(
        question,
        answer
    )

    return redirect("/admin")

@app.route("/add_order", methods=["POST"])
def add_order_route():

    order_id = request.form["order_id"]

    customer_name = request.form["customer_name"]

    status = request.form["status"]

    location = request.form["location"]

    delivery_date = request.form["delivery_date"]

    add_order(
        order_id,
        customer_name,
        status,
        location,
        delivery_date
    )

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)