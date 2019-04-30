# _*_ coding: utf-8 _*_

from flask import Flask, request, session, render_template, redirect, url_for, abort, make_response
from pymongo import MongoClient



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/user/<username>')
def showUserProfile(username):
    app.logger.debug('RETRIEVE DATA - USER ID : %s' % username)
    app.logger.debug('RETRIEVE DATA - Check Compelete')
    app.logger.warn('RETRIEVE DATA - Warning... User Not Found.')
    app.logger.error('RETRIEVE DATA - ERR! User unauthenification.')
    return 'USER : %s' % username



@app.route('/user/id/<int:userId>')
def showUserProfileById(userId):
    return 'USER ID : %d' % userId

@app.route('/account/login', methods=['POST'])
def login():
    if request.method == 'POST':
        userId = request.form['id']
        wp = request.form['wp']

        if len(userId) == 0 or len(wp) == 0:
            return userId + ', ' + wp + ' 로그인 정보를 제대로 입력하지 않았습니다.'

        session['logFlag'] = True
        session['userId'] = userId
        return session['userId'] + ' 님 환영합니다.'
    else:
        return '잘못된 접근입니다.'
app.secret_key = 'sample_secreat_key'
'''
@app.route('/user', methods=['GET'])
def getUser():
    if session.get('logFlag') != True:
        return '잘못된 접근입니다.'
    userId = session['userId']

    return '[GET][USER] USER ID : {0}'.format(userId)
'''
@app.route('/account/logout', methods=['POST','GET'])
def logout():
    session['logFlag'] = False
    session.pop('userId', None)

    return redirect(url_for('main'))

@app.errorhandler(400)
def uncaughtError(error):
    return '잘못된 사용입니다.'

@app.route('/user', methods=['GET'])
def getUser():
    if 'userId' in session:
        return '[GET][USER] USER ID : {0}'.format(session['userId'])
    else:
        abort(400)

'''
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)

    resp.headers['X-Something'] = 'A value'
    return resp
'''

@app.route('/login', methods=['POST','GET'])
def login_direct():
    if request.method == 'POST':
        return redirect(url_for('login'), code=307)
    else:
        return redirect(url_for('login'))

'''
@app.route('/mongo',methods=['GET'])
def mongoTest():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.newDatabase
    collection = db.mongoTest
    results = collection.find()
    client.close()
    return render_template('mongo.html', data=results)
'''

@app.route('/mongoInsert',methods=['GET'])
def mongoInsert():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    collection = db.contents

    new_contents = [
        {
        "product" : "냉장고",
        "dtno" : "REFA10251-1",
        "comment" : "냉장 약함",
        "reason" : "설정 온도가 약하거나 보관식품이 많아 냉기 순환이 안되어 냉장이 약할수 있습니다.",
        "point" : "5"
        },
        {
            "product": "에어컨",
            "dtno": "REAI23515-1",
            "comment": "뜨거운 바람 나옴",
            "reason": "냉매 충전이 필요합니다",
            "point": "5"
        }
    ]

    collection.insert_many(new_contents)
    results = collection.find()
    client.close()
    return render_template('contents.html', data=results)

@app.route('/contents',methods=['GET'])
def contents():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    collection = db.contents
    results = collection.find()
    client.close()
    return render_template('contents.html', data=results)

@app.route('/mongoCloud',methods=['GET'])
def mongoCloud():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.contents
    results = collection.find()
    client.close()
    return render_template('contents.html', data=results)

@app.route('/mongoCloudInsert',methods=['GET'])
def mongoCloudInsert():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.contents

    new_contents = [
        {
            "product": "냉장고",
            "dtno": "REFA10251-1",
            "comment": "냉장 약함",
            "reason": "설정 온도가 약하거나 보관식품이 많아 냉기 순환이 안되어 냉장이 약할수 있습니다.",
            "point": "5"
        },
        {
            "product": "에어컨",
            "dtno": "REAI23515-1",
            "comment": "뜨거운 바람 나옴",
            "reason": "냉매 충전이 필요합니다",
            "point": "5"
        }
    ]

    collection.insert_many(new_contents)
    results = collection.find()
    client.close()
    return render_template('contents.html', data=results)



@app.route('/mongoCloudDelete',methods=['GET'])
def mongoCloudDelete():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.contents



    collection.delete_many({"product" : "에어컨"})
    results = collection.find()
    client.close()
    return render_template('contents.html', data=results)



@app.route('/mongoCloudEditor',methods=['GET'])
def mongoCloudEditor():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.contents

    results = collection.find()
    client.close()
    return render_template('editor.html', data=results)


@app.route('/save',methods=['POST'])
def save():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.editor

    collection.insert({
            "username": request.form['username'],
            "editordata": request.form['editordata']
        })


    results = collection.find()
    client.close()
    return render_template('list.html', data=results)


@app.route('/list',methods=['GET'])
def list():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.editor


    results = collection.find()
    client.close()
    return render_template('list.html', data=results)


@app.route('/main',methods=['GET'])
def main():

    uri = "mongodb+srv://?retryWrites=true";
    client = MongoClient("mongodb+srv://admin:admin@cluster0-qokzw.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.editor


    results = collection.find()
    client.close()
    return render_template('main.html', data=results)



if __name__ == '__main__':
    app.debug = True
    app.run()

