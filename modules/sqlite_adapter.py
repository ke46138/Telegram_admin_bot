import sqlite3
from datetime import datetime
import config

def init_tables():
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('''
CREATE TABLE IF NOT EXISTS mute_table (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
time_unmute INTEGER NOT NULL,

chatid INTEGER NOT NULL,
reason TEXT NOT NULL
)
''') # seconds INTEGER NOT NULL,
        cursor.execute('''
CREATE TABLE IF NOT EXISTS warn_table (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
warns INTEGER NOT NULL,
time_last_warn INTEGER NOT NULL,
chatid INTEGER NOT NULL,
reason TEXT NOT NULL
)
''')
        cursor.execute('''
CREATE TABLE IF NOT EXISTS users_table (
id INTEGER PRIMARY KEY,
chatid INTEGER NOT NULL
)
''')
        connection.commit()

def mute_user(userid, username, seconds, chatid, reason):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM mute_table WHERE id = ? AND chatid = ?', (userid, chatid,))
        result = cursor.fetchall()
        if result == []:
            time = int(datetime.now().timestamp()) + seconds
            cursor.execute('INSERT INTO mute_table (id, username, time_unmute, chatid, reason) VALUES (?, ?, ?, ?, ?)', (userid, username, time, chatid, reason))
            connection.commit()

def unmute_user(userid, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM mute_table WHERE id = ? AND chatid = ?', (userid, chatid,))
        result = cursor.fetchall()
        if result != []:
            cursor.execute('DELETE FROM mute_table WHERE id = ? AND chatid = ?', (userid, chatid))
            connection.commit()

def add_warn(userid, username, chatid, reason):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM warn_table WHERE id = ? AND chatid = ?', (userid, chatid,))
        result = cursor.fetchone()
        time = int(datetime.now().timestamp())
        if result == [] or result == None:
            cursor.execute('INSERT INTO warn_table (id, username, warns, time_last_warn, chatid, reason) VALUES (?, ?, ?, ?, ?, ?)', (userid, username, 1, time, chatid, reason))
            connection.commit()
            return 1
        else:
            warns = result[2]
            cursor.execute('UPDATE warn_table SET warns = ? WHERE id = ? AND chatid = ?', (warns + 1, userid, chatid))
            connection.commit()
            return warns
        
def unwarn(userid, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM warn_table WHERE id = ? AND chatid = ?', (userid, chatid,))
        result = cursor.fetchone()
        if result != [] or result != None:
            cursor.execute('DELETE FROM warn_table WHERE id = ? AND chatid = ?', (userid, chatid))
            connection.commit()

def add_user(id, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users_table (id, chatid) VALUES (?, ?)', (id, chatid))
        connection.commit()

def remove_user(id, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users_table WHERE id = ? AND chatid = ?', (id, chatid))

def select_all(table):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM ?', (table))
        return cursor.fetchall()

def select_all_where(table, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table} WHERE chatid = ?', (chatid,))
        return cursor.fetchall()

def select_column_where(table, column, chatid):
    with sqlite3.connect(config.dbname) as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT {column} FROM {table} WHERE chatid = ?', (chatid,))
        return cursor.fetchall()
