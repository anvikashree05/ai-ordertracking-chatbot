# AI-Powered Order Tracking Chatbot (WISMO)

## Project Overview

This project is an AI-powered customer support chatbot designed to automate order tracking queries (WISMO - Where Is My Order?).

Customers can check delivery status, shipment location, and expected delivery dates using natural language queries.

---

## Features

- Order Tracking
- Order ID Memory
- Natural Language Order Queries
- FAQ Support
- Chat History
- Admin Dashboard
- Add FAQ Functionality
- Add Order Functionality
- Unanswered Question Logging
- TF-IDF based NLP Matching

---

## Technologies Used

- Python
- Flask
- SQLite
- Scikit-Learn
- TF-IDF
- HTML
- CSS
- JavaScript

---

## Project Structure

AI_chatbot/
│
├── app.py
├── chatbot.py
├── database.py
├── requirements.txt
├── README.md
│
├── data/
│   └── intents.json
│
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── history.html
│
└── static/
    ├── style.css
    └── script.js

---

## Example Queries

- My order ID is 12345
- Track my order
- Where is my order 12345?
- Shipment status 12345
- How do I change my delivery address?

---

## Installation

1. Clone the repository:

```bash
git clone <repository-url>