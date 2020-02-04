from flask import Blueprint, jsonify
from models.user import User
import os

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

@images_api_blueprint.route('/<user_id>', methods=['GET'])
def image(user_id):
    user = User.get_by_id(user_id)
    user.images

    a = []
    for image in user.images:
        a.append(image.get_url())
    
    return jsonify(a)                             