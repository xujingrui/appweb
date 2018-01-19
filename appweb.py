#encoding: utf-8
from flask import Flask,render_template,url_for,redirect,session
import config
from flask import request
from models import UserModel
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        admin = app.config.get('ADMIN')
        adminpassword = app.config.get('ADMINPASSWORD')
        if request.form.get('username') == admin and request.form.get('password') == adminpassword:
            session['user_id'] = admin
            return render_template('home.html')
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.query.filter(UserModel.username == username,UserModel.password == password).first()
        if user:
            session['user_id'] = user.id
            #30天免密码登录
            #session.permanent = True
            return render_template('home.html')
        else:
            return u'用户和密码错误，请重新输入！'
    else:
        return render_template('login.html')


@app.route('/logout/')
def logout():
    #session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/user/<id>',methods=['GET','POST'])
def user(id):
    if id == 'user_list':
        if request.method == 'POST':
            username = request.form.get('username1')
            telephone = request.form.get('telephone')
            mail = request.form.get('mail')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            if password1 != password2 :
                return u'两次密码输入错误，请重新填写！'
            else:
                user = UserModel(username=username,telephone=telephone,mail=mail,password=password1,status='激活')
                db.session.add(user)
                db.session.commit()
                return '注册成功'
        else:
            items = UserModel.query.all()[:]
            return render_template('user_list.html',items=items)


    if id == 'user_login_log':
        return render_template('user_login_log.html')
    else:
        return '无效'




@app.route('/CMDB/')
def CMDB():
    return render_template('cmdb.html')


@app.context_processor
def context_processor():
    user_id = session.get('user_id')
    user = UserModel.query.filter(UserModel.id == user_id).first()
    if user_id:
        return {'user':user}
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)

