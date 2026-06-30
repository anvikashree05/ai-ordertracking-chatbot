import re
import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import (
    save_memory,
    get_memory,
    get_order,
    save_unanswered_question,
    get_faq_answer
)

with open("data/intents.json", "r") as file:
    data = json.load(file)

patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(patterns)


def get_response(message):

    message = message.lower().strip()

    faq_answer = get_faq_answer(message)

    if faq_answer:
     return faq_answer

    # ==========================
    # NAME MEMORY
    # ==========================

    if "my name is" in message:

        name = message.replace(
            "my name is",
            ""
        ).strip()

        save_memory(
            "name",
            name
        )

        return f"Nice to meet you, {name.title()}!"

    if "what is my name" in message:

        name = get_memory("name")

        if name:
            return f"Your name is {name.title()}."

        return "I don't know your name yet."

    # ==========================
    # ORDER ID MEMORY
    # ==========================

    if "my order id is" in message:

        order_id = message.replace(
            "my order id is",
            ""
        ).strip()

        save_memory(
            "order_id",
            order_id
        )

        return f"I'll remember your Order ID: {order_id}"

    if "what is my order id" in message:

        order_id = get_memory(
            "order_id"
        )

        if order_id:
            return f"Your Order ID is {order_id}."

        return "I don't know your Order ID yet."

    # ==========================
    # TRACK SAVED ORDER
    # ==========================

    if "track my order" in message:

        order_id = get_memory(
            "order_id"
        )

        if not order_id:
            return "Please tell me your Order ID first."

        order = get_order(order_id)

        if not order:
            return "Order not found."

        return (
            f"Order ID: {order[0]}\n"
            f"Customer: {order[1]}\n"
            f"Status: {order[2]}\n"
            f"Location: {order[3]}\n"
            f"Delivery Date: {order[4]}"
        )

    # ==========================
    # NATURAL LANGUAGE ORDER TRACKING
    # ==========================

    order_match = re.search(
        r"\b\d{5}\b",
        message
    )

    if order_match and (
        "order" in message
        or "package" in message
        or "shipment" in message
    ):

        order_id = order_match.group()

        order = get_order(order_id)

        if not order:
            return "Order not found."

        return (
            f"Order ID: {order[0]}\n"
            f"Customer: {order[1]}\n"
            f"Status: {order[2]}\n"
            f"Location: {order[3]}\n"
            f"Delivery Date: {order[4]}"
        )

    # ==========================
    # TF-IDF FALLBACK
    # ==========================

    user_vector = vectorizer.transform(
        [message]
    )

    similarity = cosine_similarity(
        user_vector,
        X
    )

    best_match_index = similarity.argmax()

    score = similarity[0][best_match_index]
    if score < 0.6:

     save_unanswered_question(message)

     return (
        "Sorry, I couldn't understand that. "
        "Could you rephrase your question?"
    )
    matched_tag = tags[
        best_match_index
    ]

    for intent in data["intents"]:

        if intent["tag"] == matched_tag:

            return random.choice(
                intent["responses"]
            )

    return (
        "Sorry, I couldn't understand that."
    )
