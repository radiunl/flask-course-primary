#!coding:utf8
from flask import render_template, redirect, url_for, flash, request
from userauth_demo import app
# 从userauth_demo.forms中导入LoginForm类
from userauth_demo.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from userauth_demo.models import User
from userauth_demo.forms import registerForm
from userauth_demo import db, bcrypt


# 添加视图函数渲染主页内容
@app.route('/')
@login_required
def index():
    return render_template('index.html', title='第五天')


# 添加视图函数渲染表单登陆内容
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 对类LoginForm的实例
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextpage = request.args.get('next')
            if nextpage:
                return redirect(nextpage)
            else:
                url = url_for('index')
                return redirect(url)
        else:
            flash('登陆不成功，请检查邮箱和密码！', 'danger')
    return render_template('login.html', title='第五天', html_form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登陆！', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="第五天", html_form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))






