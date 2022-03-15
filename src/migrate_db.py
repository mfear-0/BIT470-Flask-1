import sqlite3

def init_db():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL, username text PRIMARY KEY, password text, date_joined Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    #cur.execute("INSERT OR IGNORE INTO users VALUES (87, 'user1', '1234', '2022-01-02')")
    #cur.execute("INSERT OR IGNORE INTO users VALUES (92, 'user3', 'abcd', '2022-02-01')")
    cur.execute('CREATE TABLE IF NOT EXISTS rooms(id INTEGER NOT NULL, roomnumber text PRIMARY KEY)')
    cur.execute('CREATE TABLE IF NOT EXISTS token(id INTEGER NOT NULL, tokenid text PRIMARY KEY)')
    cur.execute('CREATE TABLE IF NOT EXISTS staff(staffid INTEGER NOT NULL PRIMARY KEY, id INTERGER NOT NULL, staffname text, phonenumber text, email text, address text)')
    cur.execute('CREATE TABLE IF NOT EXISTS assignments(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, staffid INTEGER NOT NULL, taskid INTEGER NOT NULL, roomid INTEGER NOT NULL)')
    
    # Arica: The Tasks table and the default ten tasks.
    cur.execute('CREATE TABLE IF NOT EXISTS tasks(taskid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, taskname text)')
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (1, 'Changing linens on beds.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (2, 'Serving meals.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (3, 'Feeding patient.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (4, 'Handing out medication.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (5, 'Taking patient vitals.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (6, 'Helping patient with hygiene and dressing.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (7, 'Turning and repositioning patient.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (8, 'Restock supplies in room.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (9, 'Sanitize room.')")
    cur.execute("INSERT OR IGNORE INTO tasks VALUES (10, 'Help patient get into bed or wheelchair.')")

    con.commit()
    con.close()