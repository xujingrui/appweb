#encoding: utf-8

from exts import db
import shortuuid,datetime

#id,用户，手机，密码，邮件，创建时间，退出时间，状态
class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(30),nullable=False)
    telephone = db.Column(db.String(15),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    mail = db.Column(db.String(30),nullable=False)
    ctime = db.Column(db.DateTime,default=datetime.datetime.now)
    etime = db.Column(db.String(20),nullable=True)
    status = db.Column(db.String(10),default='激活')


#id,用户，登录地址，登录时间
class UserLoginLogModel(db.Model):
    __tablename__ = 'userloginlog'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(30),nullable=False)
    ipaddr = db.Column(db.String(50),nullable=False)
    ctime = db.Column(db.DateTime,default=datetime.datetime.now)
    status =  db.Column(db.String(10),nullable=False)



#id,用户，操作时间，操作内容
class UserOperationLogModel(db.Model):
    __tablename__ = 'useroperationlog'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(30),nullable=False)
    ctime = db.Column(db.DateTime, default=datetime.datetime.now)
    operation = db.Column(db.String(100),nullable=False)


#id,名称，购买时间，操作系统，IP地址，CPU核心数，内存，硬盘，使用状态
class CmdbAssetModel(db.Model):
    __tablename__ = 'cmdbasset'
    id = db.Column(db.String(100), primary_key=True,default=shortuuid.uuid)
    name = db.Column(db.String(30),nullable=False)
    ctime = db.Column(db.String(20),nullable=True)
    system = db.Column(db.String(20),nullable=False)
    ipaddr = db.Column(db.String(50),nullable=False)
    core_number = db.Column(db.String(3),nullable=False)
    memory = db.Column(db.String(3),nullable=False)
    disk = db.Column(db.String(50),nullable=False)
    status = db.Column(db.String(10),default='在用')

#id,主机名称,主机地址,主机端口
class DockerList(db.Model):
    __tablename__ = 'hostlist'
    id = db.Column(db.String(100), primary_key=True,default=shortuuid.uuid)
    hostname = db.Column(db.String(30),nullable=False)
    hostipaddr = db.Column(db.String(50),nullable=False)
    hostport = db.Column(db.String(5),nullable=False)






