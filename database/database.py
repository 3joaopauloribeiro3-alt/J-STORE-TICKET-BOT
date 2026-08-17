import sqlite3
import os

DATABASE_FILE = "database/jstore.db"


def connect():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def initialize():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            user_id INTEGER,
            channel_id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            ticket_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_ticket(
    user_id,
    channel_id,
    guild_id,
    ticket_type
):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (user_id, channel_id, guild_id, ticket_type)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            channel_id,
            guild_id,
            ticket_type
        )
    )

    connection.commit()
    connection.close()


def get_ticket(value, by_user=False):
    connection = connect()
    cursor = connection.cursor()

    if by_user:
        cursor.execute(
            """
            SELECT user_id, channel_id, guild_id, ticket_type
            FROM tickets
            WHERE user_id = ?
            """,
            (value,)
        )
    else:
        cursor.execute(
            """
            SELECT user_id, channel_id, guild_id, ticket_type
            FROM tickets
            WHERE channel_id = ?
            """,
            (value,)
        )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    return {
        "user_id": row[0],
        "channel_id": row[1],
        "guild_id": row[2],
        "ticket_type": row[3]
    }


def delete_ticket(channel_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tickets WHERE channel_id = ?",
        (channel_id,)
    )

    connection.commit()
    connection.close()
