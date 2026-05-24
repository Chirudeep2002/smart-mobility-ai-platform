import sqlite3
import os
import bcrypt
import re


# =====================================================
# DATABASE
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "users.db")


# =====================================================
# CREATE USERS TABLE
# =====================================================

def init_users_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,
        
        preference TEXT DEFAULT 'Balanced'
    )
    """)

    conn.commit()

    conn.close()


# =====================================================
# PASSWORD VALIDATION
# =====================================================

def is_strong_password(password):

    pattern = (
        r"^(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@$!%*?&])"
        r"[A-Za-z\d@$!%*?&]{8,}$"
    )

    return re.match(pattern, password)


# =====================================================
# CREATE USER
# =====================================================

def create_user(username, password):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


# =====================================================
# LOGIN VALIDATION
# =====================================================

def validate_user(username, password):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        stored_password = result[0]

        return bcrypt.checkpw(
            password.encode(),
            stored_password
        )

    return False

# =====================================================
# UPDATE USER PREFERENCE
# =====================================================

def update_preference(username, preference):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET preference = ?
        WHERE username = ?
        """,
        (preference, username)
    )

    conn.commit()

    conn.close()

# =====================================================
# GET USER PREFERENCE
# =====================================================

def get_preference(username):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT preference
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return "Balanced"