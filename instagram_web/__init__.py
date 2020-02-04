import os
from app import app
from flask import render_template, session
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.session.routes import session_blueprint
from instagram_web.blueprints.images.routes import images_blueprint
from instagram_web.blueprints.payments.routes import payments_blueprint
from instagram_web.blueprints.follow.routes import follow_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from flask_login import login_required
from instagram_web.helpers.google_oauth import oauth
import config

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)


app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(session_blueprint, url_prefix="/session")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(payments_blueprint, url_prefix="/payments")
app.register_blueprint(follow_blueprint, url_prefix="/follow")


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    if 'user_id' in session:
        current_user = User.get_by_id(session['user_id'])
        return render_template('404.html', current_user=current_user), 404
    return render_template('404.html'), 404

# @app.route("/")
# def home():
#     if 'user_id' in session:
#         current_user = User.get_by_id(session['user_id'])
#         return render_template('home.html', current_user=current_user)
#     return render_template('home.html')

@app.route("/a")
@login_required
def a():
    return 'a'

@app.route("/")
def home():
    return render_template('home.html', aws_domain=os.getenv('AWS_DOMAIN'), users=User.select())