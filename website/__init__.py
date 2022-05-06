from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path 
from flask_login import LoginManager

# defining a new database (database object) 
db = SQLAlchemy()
# Picking a database name
DB_NAME = "database.db" 

def create_app():
    # initializing the app
    app = Flask(__name__)  

    # initializing secret key
    app.config['SECRET_KEY'] = '64629JEtGBkyWIj3O3MaMOo32'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 


    # registering the blueprints
    from .views import views
    from .auth import auth 


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User, Note   

    create_database(app)
    
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) 


    return app 


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
