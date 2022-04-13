from datetime import datetime
import sqlite3


def record(message):
    connect = sqlite3.connect('data/users.db')
    connect.commit()
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS logins(
                            id INTEGER,
                            name TEXT,
                            GMT DATE
                    )""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM logins WHERE id = {people_id}")
    data = cursor.fetchone()
    ts = int(message.date)
    dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if data is None:
        sql = "insert into logins values (?, ?, ?)"
        cursor.execute(sql, (message.chat.id, message.from_user.first_name, dt))
        connect.commit()