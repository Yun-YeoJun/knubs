import pymysql
from user import User
from datetime import datetime
from db import *
def signUp(args, bcrypt):
    user = makeUser(args, bcrypt)
    sql = f"""INSERT INTO KNUBS_DB.USER (USERID, PASSWORD, NAME, BIRTHDAY, PHONENUM, STUDENTID, REGDATE) VALUES ('{user.userId}', '{user.password}', '{user.name}', '{user.birthday}', '{user.phoneNum}', '{user.studentId}', '{user.regDate}');"""
    return executeInsertSQL(sql)

def makeUser(args,bcrypt):
    user = User()
    user.setUserId(args['userId'])
    user.setPassword(bcrypt.generate_password_hash(args['password'].encode('utf-8')).decode())
    user.setName(args['name'])
    user.setBirthDay(args['birthday'])
    user.setPhoneNum(args['phoneNum'])
    user.setStudentId(args['studentId'])
    user.setRegDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return user
