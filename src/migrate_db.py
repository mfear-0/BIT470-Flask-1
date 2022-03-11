import sqlite3

def init_db():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL, username text PRIMARY KEY, password text, date_joined Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    #cur.execute("INSERT OR IGNORE INTO users VALUES (87, 'user1', '1234', '2022-01-02')")
    #cur.execute("INSERT OR IGNORE INTO users VALUES (92, 'user3', 'abcd', '2022-02-01')")
    cur.execute('CREATE TABLE IF NOT EXISTS rooms(id INTEGER NOT NULL, roomnumber text PRIMARY KEY)')
    cur.execute('CREATE TABLE IF NOT EXISTS token(id INTEGER NOT NULL, tokenid text PRIMARY KEY)')
    con.commit()
    con.close()