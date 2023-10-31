from flask import Flask, render_template, request, redirect, flash, session, escape
from signUp import *
from flask_bcrypt import Bcrypt
from login import checkUser, getUserInfo
from write import insertLetterToDb
from letter import *
from user import *

app = Flask(__name__)

f = open("key.txt", 'r')
key = f.readline()
f.close()

app.config['SECRET_KEY'] = key
app.config['BCRYPT_LEVEL'] = 10
app.secret_key = key

bcrypt = Bcrypt(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userId' in session:
        return redirect("/")

    if request.method == 'GET':
        return render_template("login.html")
    else:
        userId = request.form.get('userId')
        password = request.form.get('password')
        if checkUser(userId, password, bcrypt) == True:
            session.clear()
            session['userId'] = userId
            userInfo = getUserInfo(userId)[0]
            nameIdx = 3
            studentIdIdx = 6
            session['name'] = userInfo[nameIdx]
            session['studentId'] = userInfo[studentIdIdx]
            return redirect('/')
        else:
            flash("아이디와 비밀번호를 다시 입력해주세요")
            return redirect('/login')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("sign-up.html")
    else:
        signUpSuccess = signUp(request.form.to_dict(), bcrypt)

        if signUpSuccess:
            flash("회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect('/login')
        else:
            flash("아이디가 중복됩니다. 중복되지 않는 아이디로 다시 가입해주세요.")
            return redirect('/sign-up')


@app.route('/')
def home():
    if 'userId' in session:

        if session['userId'] == 'knubs':
            letters = getAllLetter()
            users = getAllUser()
            userIdToStudentId = {}

            for user in users:
                userIdToStudentId[user[1]] = user[6]

            return render_template("admin-home.html", letters=letters, userIdToStudentId=userIdToStudentId)
        else:
            letters = getUserLetter(session['userId'])
            return render_template("home.html", letters=letters, studentId=session['studentId'])
    else:
        return redirect("/login")

@app.route('/user-list')
def userList():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    if session['userId'] != 'knubs':
        flash("접근 권한이 없습니다.")
        return redirect('/')
    users = getAllUser()
    return render_template("admin-user-list.html", users=users)

@app.route('/write', methods=["GET", "POST"])
def write():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    if request.method == "GET":
        return render_template("write.html")
    else:
        letterTitle = request.form.get("letter-title")
        musicTitle = request.form.get("music-title")
        singer = request.form.get("singer")
        letterContent = request.form.get("letter-content")
        anonymous = request.form.get("anonymous")
        insertLetterToDb(session['userId'], session['name'], letterTitle, musicTitle, singer, letterContent, anonymous)
        flash("사연이 정상적으로 등록되었습니다.")
        return redirect('/')

@app.route("/letter", methods=["GET"])
def letter():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    letterId = request.args.get('id', '-1')

    if letterId == -1:
        flash("잘못된 주소입니다.")
        return redirect('/')

    letterById = getLetterById(letterId)

    if len(letterById) == 0:
        flash("해당하는 ID의 사연이 없습니다.")
        return redirect('/')

    if len(letterById) > 1:
        flash("해당하는 ID의 사연이 2개 이상입니다. 관리자에게 문의 바랍니다.")
        return redirect('/')

    letterById = letterById[0]

    return render_template("letter.html",
                           id=letterById[0], name=letterById[2], letterTitle=letterById[3], musicTitle=letterById[4],
                           singer=letterById[5], letterContent=letterById[6], createTime=letterById[7], anonymous=letterById[8])

@app.route("/delete", methods=["GET"])
def delete():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')
    id = request.args.get("id", -1)

    if id == -1 or (not id.isdecimal()):
        flash("잘못된 삭제 요청입니다.")
        return redirect('/')

    userId = getUserIdById(id)

    if len(userId) == 0 or len(userId[0]) == 0:
        flash("삭제 과정에서 오류가 발생하였습니다. 관리자에게 문의 바랍니다.")
        return redirect("/")

    userId = userId[0][0]

    if session['userId'] != userId and session['userId'] != "knubs":
        flash("삭제 권한이 없습니다.")
        return redirect('/')

    if not deleteLetterById(int(id)):
        flash("삭제 과정에서 오류가 발생하였습니다. 관리자에게 문의 바랍니다.")
    else:
        flash("삭제가 완료되었습니다.")

    return redirect('/')


@app.route('/my-page', methods=['GET'])
def myPage():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    userId = session['userId']
    user = getUserByUserId(userId)

    if len(user) == 0:
        flash("잘못된 접근입니다.")
        return redirect('/')

    user = user[0]

    if user[1] != userId:
        flash("마이 페이지 접근 과정에서 오류가 발생했습니다.")
        return redirect("/")

    letterNum = len(getLetterByUserId(userId))
    if session['userId'] == 'knubs':
        return render_template("admin-my-page.html", id=user[0], name=user[3], studentId=user[6], letterNum=letterNum)
    else:
        return render_template("my-page.html", id=user[0], name=user[3], studentId=user[6], letterNum=letterNum)


@app.route('/logout', methods=['GET'])
def logout():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    session.pop('userId', None)
    flash("로그아웃 되었습니다.")
    return redirect('/')

@app.route('/cancel-account', methods=['GET'])
def cancelAccount():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    if session['userId'] == 'knubs':
        flash("관리자 계정은 탈퇴할 수 없습니다.")
        return redirect('/')

    if not deleteUserByUserId(session['userId']):
        flash("탈퇴 과정에서 문제가 발생하였습니다. 관리자에게 문의 바랍니다.")
        return redirect('/')

    else:
        session.clear()
        flash("탈퇴되었습니다.")
        return redirect('/')

@app.route('/cancel-member-account', methods=['GET'])
def cancelMemberAccount():
    if 'userId' not in session:
        flash("로그인을 해주세요.")
        return redirect('/login')

    if session['userId'] != 'knubs':
        flash("접근 권한이 없습니다.")
        return redirect('/')

    userId = request.args.get('user-id', -1)

    if userId == -1:
        flash("잘못된 요청입니다.")
        return redirect('/')

    if userId == 'knubs':
        flash("관리자 계정은 삭제할 수 없습니다.")
        return redirect('/user-list')

    if not deleteUserByUserId(userId):
        flash("탈퇴 과정 중 문제가 생겼습니다.")
        return redirect('/user-list')
    else:
        flash("탈퇴 완료")
        return redirect('/user-list')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
