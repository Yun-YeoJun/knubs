from db import *
from letter import *

# USERID, PASSWORD, NAME, BIRTHDAY, PHONENUM, STUDENTID, REGDATE
class User:
    def setUserId(self, userId):
        self.userId = userId
    def setPassword(self, password):
        self.password = password
    def setName(self, name):
        self.name = name
    def setBirthDay(self, birthday):
        self.birthday = birthday
    def setPhoneNum(self, phoneNum):
        self.phoneNum = phoneNum
    def setStudentId(self, studentId):
        self.studentId = studentId
    def setRegDate(self, regDate):
        self.regDate = regDate


def getUserByUserId(userId):
    sql = f"""SELECT * FROM KNUBS_DB.USER WHERE USERID='{userId}'"""
    return executeSelectSQL(sql)


def deleteUserByUserId(userId):
    letters = getLetterByUserId(userId)
    # if len(letters):
    #     return False
    returnValue = False
    try:
        db = getDbConnection()
        cursor = db.cursor()
        for letter in letters:
            id = letter[0]
            sql = f"""DELETE FROM KNUBS_DB.LETTER WHERE ID={id};"""
            cursor.execute(sql)
        sql = f"""DELETE FROM KNUBS_DB.USER WHERE USERID='{userId}';"""
        print(sql)
        cursor.execute(sql)
        db.commit()
        returnValue = True
    except Exception as e:
        print(f"""에러 코드: {e.args[0]}""")
        print(f"""에러 메세지: {e.args[1]}""")
    finally:
        db.close()
        return returnValue


def getAllUser():
    sql="SELECT * FROM KNUBS_DB.USER"
    return executeSelectSQL(sql)
