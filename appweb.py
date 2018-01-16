#encoding: utf-8
from flask import Flask,render_template,url_for,redirect
import config
from flask import request

app = Flask(__name__)
app.config.from_object(config)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin':
            return render_template('base.html')
        else:
            return '登录失败'
    else:
        return render_template('login.html')



@app.route('/user/<id>')
def user(id):
    if id == 'user_list':
        return render_template('user_list.html')
    if id == 'user_login_log':
        return render_template('user_login_log.html')
    else:
        return '无效'




@app.route('/CMDB/')
def CMDB():
    return render_template('cmdb.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)
