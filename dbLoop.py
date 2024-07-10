import threading
import requests
import sqlite3
import time

def RunLoop():
    conn = sqlite3.connect('transactions.db')

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS long_string
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, is_checked INTEGER,url TEXT)''')

    while(True):
        time.sleep(3)
        # Retrieve all the rows where "is_checked" is 0
        cursor.execute("SELECT id, url, text FROM long_string WHERE is_checked = 0")
        rows = cursor.fetchall()
        # Loop through the rows and send the data to a server
        for row in rows:
            id, url, response = row
            data = {'data': response}
            response = requests.post(url, data=data)
            if response.status_code == 200:
                cursor.execute("UPDATE long_string SET is_checked = 1 WHERE id = ?", (id,))
                conn.commit()
                print(f"Successfully sent data for row {id}")
            else:
                print(f"Failed to send data for row {id}")
                
            time.sleep(3)


threading.Thread(target=RunLoop).start()