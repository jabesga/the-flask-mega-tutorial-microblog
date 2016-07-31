from flask import render_template, flash, redirect, url_for, request, session
from app import app, oauth, login_manager, db
from .forms import LoginForm
from .models import User
from flask_login import login_user

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key='KrMi8HNPZsDWDdTr7fQlDwaps',
                           consumer_secret='fjXTIUkVWxcwACpc3ftiWrUAcaZlD33vVhM9uXsDS1nBpiuXfO')

facebook = oauth.remote_app('facebook',
                            consumer_key='529433733913526',
                            consumer_secret='ed6fe9df4f2eb1122f8e4d5bcb3c5bbc',
                            request_token_params={'scope': 'email'},
                            base_url='https://graph.facebook.com',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            access_token_method='GET',
                            authorize_url='https://www.facebook.com/dialog/oauth')

@login_manager.user_loader
def load_user(id):
    # It should return None (not raise an exception) if the ID is not valid.
    # (In that case, the ID will manually be removed from the session and processing will continue.)
    return User.query.get(int(id))

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

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash_message = 'Login requested for OpenID="{}", remember_me={}'.format(form.openid.data, form.remember_me.data)
        flash(flash_message)
        return redirect('/')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/login/<provider>/')
def login_with(provider):
    if provider == 'twitter':
        return twitter.authorize(callback=url_for('twitter_authorized', _external=True))
    elif provider == 'facebook':
        return facebook.authorize(callback=url_for('facebook_authorized', _external=True))
    else:
        return redirect('/login')

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.route('/login/twitter/authorized/')
def twitter_authorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect('/login')
    else:
        session['twitter_oauth'] = resp

    social_id = 'twitter$' + str(resp['user_id'])
    nickname = resp['screen_name']
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=nickname)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    flash('You were signed in as %s' % str(user.nickname))
    return redirect('/')

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

@app.route('/login/facebook/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        error_message = 'Access denied: reason={} error={}'.format(request.args['error_reason'], request.args['error_description'])
        flash(error_message)
        return redirect('/login')

    session['facebook_token'] = (resp['access_token'], '')
    flash('You were signed sucessfully')
    return redirect('/')
