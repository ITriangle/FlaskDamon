#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from logging import Formatter

from flask import Flask, session, redirect, url_for, escape, request


def init_mail_handler(app_logger,flask_app=None):
    '''
    邮件发送日志，发送的级别为 ERROR
    :param app_logger: 
    :return: 
    '''
    SMTP_HOST = 'smtp.163.com'
    SMTP_PORT = 25

    FROM = 'triangle@163.com'
    PASS = 'password'
    TO = ['triangle@triangle.com']

    if flask_app is None or not flask_app.debug:
        mail_handler = SMTPHandler(
            (SMTP_HOST, SMTP_PORT)
            , FROM
            , TO
            , 'YourApplication Failed'
            , (FROM, PASS))
        # 设置发送邮件的日志级别
        mail_handler.setLevel(logging.ERROR)
        # 设置邮件日志格式
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
        app_logger.addHandler(mail_handler)


def init_file_handler(app_logger,flask_app=None):
    '''
    写文件到日志，超过设置文件大小，就生成新的文件
    :param app_logger: 
    :return: 
    '''
    MAX_BYTES = 10000
    BACKUP_COUNT = 10
    if  flask_app is None or not flask_app.debug:
        logFormatter = Formatter(
            '%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)d@%(funcName)s) -> %(message)s')
        file_handler = RotatingFileHandler('foo.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        file_handler.setFormatter(logFormatter)
        file_handler.setLevel(logging.INFO)
        app_logger.addHandler(file_handler)



def init_flask_app(flask_app):
    '''
    初始化 flask app
    :return: 
    '''


    # app 的日志处理设置
    init_mail_handler(flask_app.logger,flask_app)
    init_file_handler(flask_app.logger,flask_app)

    return flask_app

app = Flask(__name__)
init_flask_app(app)

@app.route('/')
def index():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')

    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    print app.debug
    app.run()


# uwsgi运行命令:uwsgi --chdir /home/wl/PublicGitRepo/flask_demon --http 0.0.0.0:8088   --enable-threads --master --processes 4 --wsgi-file /home/wl/PublicGitRepo/flask_demon/application.py --callable app --buffer-size 32768 --virtualenv /home/wl/PublicGitRepo/flask_demon/ENV