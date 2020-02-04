import os
import braintree
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "session.new"
# login_manager.login_message="login successfull"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="t5qvmgkv3x4qbp85",
        public_key="5pvws267m4dx2cty",
        private_key="e251d5baef9ff6bd3e91f8eac3b89337"
    )
)




if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
