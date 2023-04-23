import sqlite3

def create_database():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          message TEXT)''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
