import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash
from models.user import *
from flask_login import current_user, login_required
import boto3, botocore


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('users/new.html', errors=['error 1', 'error 2'])
    


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form.get('user_password') 
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    user = User(name=user_name, password=user_password, email=user_email)

    # user.save returns either 1. 0 or 2. save into db
    if user.save() == 0:
        return render_template('users/new.html', errors=user.errors)
    else:
        flash('user signed up successful', "info")
        return redirect(url_for('home'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.name == username)
    if user != None:
        return render_template('users/show.html', user=user, aws_domain=os.getenv('AWS_DOMAIN'))
    abort(404)    


@users_blueprint.route('/', methods=["GET"])
def index():
    if 'user_id' in session:
        current_user = User.get_by_id(session['user_id'])
        users = User.select()
        return render_template('users/index.html', users=users, current_user=current_user)
    flash('Please Log in to access this page',"warning")
    return redirect(url_for('session.new'))    



@users_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('/users/edit.html')

    


@users_blueprint.route('/update', methods=['POST'])
@login_required
def update():
    new_username = request.form.get('user_name')
    new_email = request.form.get('user_email')

    user = User.get_by_id(current_user.id)
    user.newname = new_username
    user.newemail = new_email

    user.validate_update()

    if len(user.errors) == 0:
        User.update(name=user.newname, email=user.newemail).where(User.id == current_user.id).execute()
        flash('Profile Updated',"info")
        return redirect(url_for('users.show', username = user.newname))
    else:    
        return render_template('users/edit.html', errors=user.errors)

   
@users_blueprint.route('/change', methods=['GET'])
@login_required
def change():
    return render_template('users/change.html')

@users_blueprint.route('/perform_change', methods=['POST'])
@login_required
def perform_change():
    newfile = request.files.get('newprof_img')
   
    if newfile.content_type == 'image/jpeg' or newfile.content_type == 'image/png':
        if newfile.content_type == 'image/jpeg':
           extension='.jpg'
        else:
            extension = '.png'
        file_name = f'{current_user.id}_prof_pic' + extension

        User.update(profileimg=file_name).where(User.id==current_user.id).execute()


        s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        # s3 = boto3.client('s3')
        s3.upload_fileobj(newfile, os.getenv('AWS_BUCKET_NAME'), file_name, ExtraArgs={"ACL": "public-read","ContentType": newfile.content_type})
        flash("successfully uploaded image", "info")

        return redirect(url_for('users.show', username=current_user.name))
    return render_template('users/change.html', error="Please upload an appropriate file")
   