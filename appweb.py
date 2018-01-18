#encoding: utf-8
from flask import Flask,render_template,url_for,redirect
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
        if request.form.get('username') == 'admin':
            return render_template('home.html')
        else:
            return '登录失败'
    else:
        return render_template('login.html')



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

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)
