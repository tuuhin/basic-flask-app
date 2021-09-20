from flask import Flask
from flask_login import LoginManager
import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def create_app():
    fl_app = Flask(__name__)

    fl_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db' 

    fl_app.config['SECRET_KEY'] = '' #your secret key here...
    db.init_app(fl_app)
    

    from .views import views
    from .auth import auth
    fl_app.register_blueprint(views,url_preffix='/')
    fl_app.register_blueprint(auth,url_preffix='/')

    from .models import User,Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(fl_app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_db(fl_app)
    return fl_app

def create_db(app):
    if not os.path.exists('webpage/storage.db'):
        db.create_all(app=app)
