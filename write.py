from db import *
from datetime import datetime

def insertLetterToDb(userId, userName, letterTitle, musicTitle, singer, letterContent, anonymous):
    sql = f"""INSERT INTO KNUBS_DB.LETTER (USERID, USERNAME, LETTER_TITLE, MUSIC_TITLE, SINGER, LETTER_CONTENT, CREATE_DATE, ANONYMOUS) 
    VALUES ('{userId}', '{userName}', '{letterTitle}', '{musicTitle}', '{singer}', '{letterContent}', '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', {anonymous})"""

    executeInsertSQL(sql)
