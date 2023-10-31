from db import *


def checkUser(userId, password, bcrypt):
    data = getUserInfo(userId)

    if len(data) == 0:
        return False

    userFromDb = data[0]
    passwordIdx = 2
    if bcrypt.check_password_hash(bytes(userFromDb[passwordIdx].encode('utf-8')), password.encode('utf-8')) == True:
        return True
    else:
        return False


def getUserInfo(userId):
    sql = f"""SELECT * FROM KNUBS_DB.USER WHERE USERID='{userId}';"""

    return executeSelectSQL(sql)
