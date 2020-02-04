from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.user import User

follow_blueprint = Blueprint('follow',
                            __name__,
                            template_folder='templates')


@follow_blueprint.route('/', methods=["GET"])
def index():
    return "Follow index" 

@follow_blueprint.route('/show', methods=["GET"])
def show():
    return render_template('follow/show.html')     

@follow_blueprint.route('/follow/<user_id>' , methods=["GET"])
@login_required
def follow(user_id):
    user = User.get_by_id(user_id)
    current_user.follow(user)
    flash('Follow Success', "success")
    return redirect(url_for('users.show', username=user.name))

@follow_blueprint.route('/unfollow/<user_id>' , methods=["GET"])
@login_required
def unfollow(user_id):
    user = User.get_by_id(user_id)
    current_user.unfollow(user)
    flash('Unfollow Success',"danger")
    return redirect(url_for('users.show', username=user.name))


@follow_blueprint.route('/cancel/<user_id>' , methods=["GET"])
@login_required
def cancel(user_id):
    user = User.get_by_id(user_id)
    current_user.cancel_request(user)
    flash('Cancel request Successful', "warning")
    return redirect(url_for('users.show', username=user.name)) 

@follow_blueprint.route('/approve/<user_id>' , methods=["GET"])
@login_required
def approve(user_id):
    user = User.get_by_id(user_id)
    current_user.approve(user)
    flash('Approved', "info")
    return redirect(url_for('users.show', username=user.name))

@follow_blueprint.route('/reject/<user_id>' , methods=["GET"])
@login_required
def reject(user_id):
    user = User.get_by_id(user_id)
    current_user.reject(user)
    flash('Rejected', "danger")
    return redirect(url_for('users.show', username=user.name))            
                          