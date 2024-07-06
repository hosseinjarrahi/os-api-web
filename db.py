import sqlite3

conn = sqlite3.connect('transactions.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS long_string
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, is_checked INTEGER,url TEXT)''')

def create(long_string,url):
    cursor.execute("INSERT INTO long_string (text,url,is_checked) VALUES (?,?,?)", (long_string,url,'0'))
    conn.commit()
