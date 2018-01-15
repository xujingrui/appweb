#encoding: utf-8
from flask import Flask,render_template,url_for
import config
from flask import request

app = Flask(__name__)
app.config.from_object(config)



@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin':
            return render_template('base.html')
        else:
            return '登录失败'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)
