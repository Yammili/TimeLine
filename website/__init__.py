from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apoloapolo'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .user import user
    from .posts import posts

    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app 

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')