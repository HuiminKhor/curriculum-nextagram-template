from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user
from instagram_web.helpers.google_oauth import oauth 

session_blueprint = Blueprint('session',
                            __name__,
                            template_folder='templates')



@session_blueprint.route('/', methods=["GET"])
def index():
    return "Session" 

@session_blueprint.route('/new', methods=["GET"])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    return render_template('/session/new.html')

@session_blueprint.route('/create', methods=["POST"])
def create():
    
    user_name = request.form.get('user_name') 
    user_password = request.form.get('user_password')

    user = User.get_or_none(User.name == user_name)

    if user != None:
        result = check_password_hash(user.password, user_password)

        if result == True:
            flash('user logged in successful', "info")
            session['user_id']= user.id
            return redirect(url_for('home'))

    return render_template('/session/new.html', errors=["Wrong username or password"]) 


@session_blueprint.route('/logout')
def logout():
    flash('successfully logged out', "danger")
    session.pop('user_id', None)
    return redirect(url_for('home'))
      
@session_blueprint.route('/create2', methods=["POST"])
def create2():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_or_none(User.name == username)

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return 'wrong'        

@session_blueprint.route('/logout2', methods=['GET'])
def logout2():
    logout_user()
    return 'logout successfully'


@session_blueprint.route('/google', methods=['GET'])
def google():
    redirect_uri = url_for('session.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)



@session_blueprint.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email'] 

    user = User.get_or_none(User.email == email) 

    login_user(user)
    if user:
        flash('logged in successfully', "info")
        return redirect (url_for('users.show', username=user.name ))
    else:
        flash('Please sign up in order to log in with google', "Warning")
        return render_template('/session/new.html')  

     




