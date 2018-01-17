#encoding: utf-8

import os

DEBUG = True

SECRET_KEY = os.urandom(64)

HOSTNAME = '172.16.0.10'
PORT     = '3306'
DATABASE = 'ops'
USERNAME = 'root'
PASSWORD = '12345678'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
