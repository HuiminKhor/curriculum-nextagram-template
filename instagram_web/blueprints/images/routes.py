import os
import boto3
import hashlib
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.image import Image


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/', methods=['GET'])
def index():
    return "images index"

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')  

@images_blueprint.route('/create', methods=['POST'])
@login_required
def create():
    file = request.files.get('upload_img')
   
    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        if file.content_type == 'image/jpeg':
           extension='.jpg'
        else:
            extension = '.png'  

        image = Image(user_id=current_user.id)
        image.save()
        hash_product = hashlib.pbkdf2_hmac('sha256', bytes([image.id]), b'salt', 100).hex()
        file_name = hash_product + extension           
        image.filename = file_name
        image.save()

        s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            # s3 = boto3.client('s3')
        s3.upload_fileobj(file, os.getenv('AWS_BUCKET_NAME'), file_name, ExtraArgs={"ACL": "public-read","ContentType": file.content_type})
        flash("successfully uploaded image", "info")

        return redirect(url_for('users.show', username=current_user.name))
    return render_template('images/new.html', error="Please upload an appropriate file")
