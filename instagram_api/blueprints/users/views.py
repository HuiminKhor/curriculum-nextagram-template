from flask import Blueprint, jsonify
from models.user import User
import os

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return jsonify(a=1,b=2,c=3)

@users_api_blueprint.route('/<user_id>', methods=['GET'])
def a(user_id):
    user = User.get_by_id(user_id)
    return jsonify(id=user.id, name=user.name, email=user.email, profile_image=os.getenv('AWS_DOMAIN') + user.profileimg)


# @users_api_blueprint.route('b/<user_id>', methods=['GET'])
# def b(user_id):
#     user = User.get_by_id(user_id)
#     user.images

#     a = []
#     for image in user.images:
#         a.append(image.get_url())
    
#     return jsonify(a)

    # return jsonify([image.get_url() for image in user.images])
    # return jsonify(id=user.id, name=user.name, image=user.email)