from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day!'
        },
        {
            'author': {'nickname': 'Martha'},
            'body': 'Sad day!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash_message = 'Login requested for OpenID="{}", remember_me={}'.format(form.openid.data, form.remember_me.data)
        flash(flash_message)
        return redirect('/')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
