import sqlite3
import time as t
from datetime import datetime
from modules import mute
from config import dbname
import logging

muteWork = True
unwarnWork = True
bot_g = ""
logging.basicConfig(level=logging.DEBUG)

def mute_ticker():
    while muteWork:
        try:
            #print("Working")
            result = []
            with sqlite3.connect(dbname) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM mute_table')
                result = cursor.fetchall()
            for user in result:
                time = user[2]
                if time <= int(datetime.now().timestamp()):
                    with sqlite3.connect(dbname) as connection:
                        cursor = connection.cursor()
                        bot_g.restrict_chat_member(
                            user[3], user[0],
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True)
                        cursor.execute('DELETE FROM mute_table WHERE id = ? AND chatid = ?', (user[0], user[3],))
                        connection.commit()
        except Exception as e:
            print(str(e))
        t.sleep(60)

def unwarn_ticker():
    while unwarnWork:
        result = []
        with sqlite3.connect(dbname) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM warn_table')
            result = cursor.fetchall()
        for user in result:
            time = user[3]
            if int(datetime.now().timestamp()) - time >= 86400:
                cursor.execute('SELECT * FROM warn_table WHERE id = ? AND chatid = ?', (user[0], user[4],))
                result = cursor.fetchall()
                if result != [] or result != None:
                    cursor.execute('DELETE FROM warn_table WHERE id = ? AND chatid = ?', (user[0], user[4],))
                    connection.commit()
                    mute.unmute(user[0], user[4])
        t.sleep(60)