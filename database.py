# ============================================================
# MEDRAG AI - DATABASE
# SQLite Database Management
# ============================================================

import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_PATH = DATABASE_DIR / "medrag.db"


# ============================================================
# CREATE DATABASE DIRECTORY
# ============================================================

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a connection to the MedRAG database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    # This allows us to access columns by name.
    connection.row_factory = sqlite3.Row

    # Enable foreign-key relationships in SQLite.
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create all required database tables.

    Tables:
    1. users
    2. conversations
    3. messages
    """

    connection = get_connection()

    cursor = connection.cursor()


    # ========================================================
    # USERS TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            created_at TEXT NOT NULL
        )
        """
    )


    # ========================================================
    # CONVERSATIONS TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )


    # ========================================================
    # MESSAGES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            conversation_id INTEGER NOT NULL,

            role TEXT NOT NULL
                CHECK(role IN ('user', 'assistant')),

            content TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
        )
        """
    )


    # ========================================================
    # INDEXES
    # ========================================================

    # Helps quickly find conversations belonging to a user.
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_conversations_user_id

        ON conversations(user_id)
        """
    )


    # Helps quickly retrieve messages from a conversation.
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_messages_conversation_id

        ON messages(conversation_id)
        """
    )


    connection.commit()

    connection.close()

    print("MedRAG database initialized successfully.")


# ============================================================
# USER DATABASE FUNCTIONS
# ============================================================

def create_user(name, email, password_hash):
    """
    Create a new user.

    Password hashing itself will be implemented in Step 2.
    This function only stores the resulting password hash.
    """

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()


    try:

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email.lower().strip(),
                password_hash,
                created_at,
            ),
        )

        connection.commit()

        user_id = cursor.lastrowid

        return user_id


    except sqlite3.IntegrityError:

        # Most likely duplicate email.
        return None


    finally:

        connection.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email):
    """
    Find a user using their email address.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            email.lower().strip(),
        ),
    )


    user = cursor.fetchone()

    connection.close()

    return user


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):
    """
    Find a user using their database ID.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (
            user_id,
        ),
    )


    user = cursor.fetchone()

    connection.close()

    return user


# ============================================================
# CREATE CONVERSATION
# ============================================================

def create_conversation(user_id, title):
    """
    Create a new conversation for a specific user.
    """

    connection = get_connection()

    cursor = connection.cursor()

    current_time = datetime.now().isoformat()


    cursor.execute(
        """
        INSERT INTO conversations (
            user_id,
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            current_time,
            current_time,
        ),
    )


    connection.commit()

    conversation_id = cursor.lastrowid

    connection.close()

    return conversation_id


# ============================================================
# GET USER CONVERSATIONS
# ============================================================

def get_user_conversations(user_id):
    """
    Return all conversations belonging to a user.

    Most recently updated conversations appear first.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM conversations
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (
            user_id,
        ),
    )


    conversations = cursor.fetchall()

    connection.close()

    return conversations


# ============================================================
# GET SINGLE CONVERSATION
# ============================================================

def get_conversation(conversation_id, user_id):
    """
    Return a conversation only if it belongs to the
    specified user.

    This is important for user privacy.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM conversations
        WHERE id = ?
        AND user_id = ?
        """,
        (
            conversation_id,
            user_id,
        ),
    )


    conversation = cursor.fetchone()

    connection.close()

    return conversation


# ============================================================
# SAVE MESSAGE
# ============================================================

def save_message(conversation_id, role, content):
    """
    Save a user or assistant message.

    role must be:
    - user
    - assistant
    """

    if role not in ["user", "assistant"]:

        raise ValueError(
            "Role must be 'user' or 'assistant'."
        )


    connection = get_connection()

    cursor = connection.cursor()

    current_time = datetime.now().isoformat()


    cursor.execute(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
            current_time,
        ),
    )


    # Update conversation timestamp so recently active
    # conversations appear at the top of the sidebar.

    cursor.execute(
        """
        UPDATE conversations
        SET updated_at = ?
        WHERE id = ?
        """,
        (
            current_time,
            conversation_id,
        ),
    )


    connection.commit()

    message_id = cursor.lastrowid

    connection.close()

    return message_id


# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

def get_conversation_messages(conversation_id):
    """
    Return all messages belonging to a conversation
    in chronological order.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (
            conversation_id,
        ),
    )


    messages = cursor.fetchall()

    connection.close()

    return messages


# ============================================================
# DELETE CONVERSATION
# ============================================================

def delete_conversation(conversation_id, user_id):
    """
    Delete a conversation only when it belongs
    to the specified user.

    Messages are automatically deleted because
    ON DELETE CASCADE is enabled.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        AND user_id = ?
        """,
        (
            conversation_id,
            user_id,
        ),
    )


    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# ============================================================
# DELETE ALL USER CONVERSATIONS
# ============================================================

def delete_all_user_conversations(user_id):
    """
    Delete all conversations belonging to a user.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM conversations
        WHERE user_id = ?
        """,
        (
            user_id,
        ),
    )


    connection.commit()

    deleted_count = cursor.rowcount

    connection.close()

    return deleted_count
    
    initialize_database()