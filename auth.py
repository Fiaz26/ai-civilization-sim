from database import cursor, conn

def create_user(email, password):
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False


def verify_user(email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    return cursor.fetchone()
