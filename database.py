import sqlite3
from datetime import datetime


def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory(
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            status TEXT,
            location TEXT,
            delivery_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unanswered_questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
""")

    conn.commit()
    conn.close()


# ==========================
# CHAT FUNCTIONS
# ==========================

def save_chat(user_message, bot_response):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO chats
        (user_message, bot_response, timestamp)
        VALUES (?, ?, ?)
        """,
        (user_message, bot_response, timestamp)
    )

    conn.commit()
    conn.close()


def get_chats():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message,
               bot_response,
               timestamp
        FROM chats
        ORDER BY id DESC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats


def clear_chats():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chats")

    conn.commit()
    conn.close()


def get_chat_count():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chats")

    count = cursor.fetchone()[0]

    conn.close()

    return count
# ==========================
# MEMORY FUNCTIONS
# ==========================

def save_memory(key, value):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO memory
        (key, value)
        VALUES (?, ?)
        """,
        (key, value)
    )

    conn.commit()
    conn.close()


def get_memory(key):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT value
        FROM memory
        WHERE key = ?
        """,
        (key,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

# ==========================
# ORDER FUNCTIONS
# ==========================
def add_order(
    order_id,
    customer_name,
    status,
    location,
    delivery_date
):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO orders
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            order_id,
            customer_name,
            status,
            location,
            delivery_date
        )
    )

    conn.commit()
    conn.close()

def get_order(order_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


# ==========================
# UNANSWERED QUESTIONS
# ==========================

def save_unanswered_question(question):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO unanswered_questions
        (question, timestamp)
        VALUES (?, ?)
        """,
        (
            question,
            timestamp
        )
    )

    conn.commit()
    conn.close()


def get_unanswered_questions():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question,
               timestamp
        FROM unanswered_questions
        ORDER BY id DESC
    """)

    questions = cursor.fetchall()

    conn.close()

    return questions

# ==========================
# FAQ FUNCTIONS
# ==========================

def add_faq(question, answer):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO faq
        (question, answer)
        VALUES (?, ?)
        """,
        (
            question.lower(),
            answer
        )
    )

    conn.commit()
    conn.close()


def get_faq_answer(question):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT answer
        FROM faq
        WHERE question = ?
        """,
        (
            question.lower(),
        )
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None