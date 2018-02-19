#encoding: utf-8
from flask import Flask,render_template,url_for,redirect,session
import config
from flask import request
from models import UserModel,DockerList,UserLoginLogModel
from exts import db
import re,requests
from docker import DockerStatus

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        admin = app.config.get('ADMIN')
        adminpassword = app.config.get('ADMINPASSWORD')
        ipaddr = request.remote_addr
        if request.form.get('username') == admin and request.form.get('password') == adminpassword:
            session['user_id'] = admin
            log = UserLoginLogModel(username=admin,ipaddr=ipaddr,status='登录成功')
            db.session.add(log)
            db.session.commit()
            return render_template('home.html')
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.query.filter(UserModel.username == username,UserModel.password == password).first()
        if user:
            session['user_id'] = user.id
            #30天免密码登录
            #session.permanent = True
            log = UserLoginLogModel(username=username,ipaddr=ipaddr,status='登录成功')
            db.session.add(log)
            db.session.commit()
            return render_template('home.html')
        else:
            log = UserLoginLogModel(username=username, ipaddr=ipaddr, status='登录失败')
            db.session.add(log)
            db.session.commit()
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
                error = u'两次密码输入错误，请重新填写！'
                items = UserModel.query.all()[:]
                return render_template('user_list.html',items=items,error=error)
            else:
                user = UserModel(username=username,telephone=telephone,mail=mail,password=password1,status='激活')
                db.session.add(user)
                db.session.commit()
                success = u'注册成功'
                items = UserModel.query.all()[:]
                return  render_template('user_list.html',items=items,success=success)
        else:
            items = UserModel.query.all()[:]
            return render_template('user_list.html',items=items)
    if id == 'user_login_log':
        items = UserLoginLogModel.query.order_by(UserLoginLogModel.ctime.desc()).all()[:]
        return render_template('user_login_log.html',items=items)

@app.route('/docker/<id>',methods=['GET','POST'])
def docker(id):
    if id == 'host_list':
        if request.method == 'POST':
            hostname = request.form.get('hostname')
            ipaddr = request.form.get('ipaddr')
            port = request.form.get('port')
            if hostname and ipaddr and port:
                p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
                if p.match(ipaddr):
                    url = 'http://%s:%s/containers/json' % (ipaddr,port)
                    try:
                        r = requests.get(url)
                        if r.status_code == 200:
                            hostlist = DockerList(hostname=hostname,hostipaddr=ipaddr,hostport=port)
                            db.session.add(hostlist)
                            db.session.commit()
                            success = u'注册成功'
                            items = DockerList.query.all()[:]
                            return render_template('hostlist.html',items=items,success=success)
                    except:
                        error = u'请输入正确的Docker地址'
                        items = DockerList.query.all()[:]
                        return render_template('hostlist.html', items=items, error=error)
                else:
                    error = u'请输入正确的IP地址'
                    items = DockerList.query.all()[:]
                    return render_template('hostlist.html',items=items,error=error)
            else:
                error = u'请输入内容'
                items = DockerList.query.all()[:]
                return render_template('hostlist.html',items=items,error=error)
        else:
            items = DockerList.query.all()[:]
            return render_template('hostlist.html',items=items)
    if id == 'container_list':
        items = DockerList.query.all()[:]
        data =  DockerStatus(items)
        return render_template('container_list.html',data=data)

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

1