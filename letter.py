from db import *


def getAllLetter():
    sql = f"""SELECT * FROM KNUBS_DB.LETTER"""
    return executeSelectSQL(sql)


def getUserLetter(userId):
    sql = f"""SELECT * FROM KNUBS_DB.LETTER WHERE USERID='{userId}'"""
    return executeSelectSQL(sql)

def getLetterById(id):
    sql = f"""SELECT * FROM KNUBS_DB.LETTER WHERE ID='{id}'"""
    return executeSelectSQL(sql)

def getUserIdById(id):
    sql = f"""SELECT USERID FROM KNUBS_DB.LETTER WHERE ID={id};"""
    return executeSelectSQL(sql)

def deleteLetterById(id):
    sql = f"""delete from KNUBS_DB.LETTER WHERE ID={id};"""
    return executeDeleteSQL(sql)

def getLetterByUserId(userId):
    sql = f"""SELECT * FROM KNUBS_DB.LETTER WHERE USERID='{userId}';"""
    return executeSelectSQL(sql)


def deleteLetterByUserId(userId):
    letters = getLetterByUserId(userId)
    if len(letters):
        return False
    returnValue = False
    try:
        db = getDbConnection()
        cursor = db.cursor()
        for letter in letters:
            id = letter[0]
            sql = f"""DELETE FROM KNUBS_DB.LETTER WHERE ID={id};"""
            cursor.execute(sql)
        db.commit()
        returnValue = True
    except Exception as e:
        print(f"""에러 코드: {e.args[0]}""")
        print(f"""에러 메세지: {e.args[1]}""")
    finally:
        db.close()
        return returnValue