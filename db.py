import pymysql

def getDbConnection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='KNUBS',
        passwd="KNUBS",
        db="KNUBS_DB",
        charset='utf8'
    )

def executeInsertSQL(sql):
    returnValue = False
    try:
        db = getDbConnection()
        cursor = db.cursor()
        print(sql)
        cursor.execute(sql)
        db.commit()
        returnValue = True
        print("INSERT 퀴리 실행 완료")
    except pymysql.IntegrityError as e:
        print(f"""에러 코드: {e.args[0]}""")
        print(f"""에러 메세지: {e.args[1]}""")
    finally:
        db.close()
        return returnValue


def executeSelectSQL(sql):
    db = getDbConnection()
    cursor = db.cursor()
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    print("SELECT 쿼리 실행 완료")
    return data

def executeDeleteSQL(sql):
    try:
        returnValue = False
        db = getDbConnection()
        cursor = db.cursor()
        print(sql)
        cursor.execute(sql)
        db.commit()
        returnValue = True
        print("DELETE 쿼리 실행 완료")
    except Exception as e:
        print(f"""에러 코드: {e.args[0]}""")
        print(f"""에러 메세지: {e.args[1]}""")
        returnValue = False
    finally:
        db.close()
        return returnValue
