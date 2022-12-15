from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = '21312$!@#!@#!@%$#^4634534&^%^*67DAWDWA321321dcscas'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost/book_final4?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['PAGE_SIZE'] = 4
app.config['COMMENT_SIZE'] = 3
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)

cloudinary.config(
            cloud_name= 'drda2ewdn',
            api_key= '997117385728161',
            api_secret= 'ptwTv6M8hsgwm5GG0s-RCgMhWW0'
)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'