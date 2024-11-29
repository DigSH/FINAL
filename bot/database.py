import sqlite3

conn = sqlite3.connect('data/interactions.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_interactions (user_id INTEGER PRIMARY KEY, interactions INTEGER, paid BOOLEAN)''')
conn.commit()

def get_user_interactions(user_id):
    c.execute('SELECT interactions FROM user_interactions WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        c.execute('INSERT INTO user_interactions (user_id, interactions, paid) VALUES (?, 0, 0)', (user_id,))
        conn.commit()
        return 0

def increment_user_interactions(user_id):
    interactions = get_user_interactions(user_id) + 1
    c.execute('UPDATE user_interactions SET interactions = ? WHERE user_id = ?', (interactions, user_id))
    conn.commit()

def reset_user_interactions(user_id):
    c.execute('UPDATE user_interactions SET interactions = 0, paid = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
