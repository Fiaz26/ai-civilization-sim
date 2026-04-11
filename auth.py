# auth.py

def create_user(cursor, conn, email, password):
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, 10)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False


def verify_user(cursor, email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    return cursor.fetchone()
