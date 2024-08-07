from flask import Flask, redirect, request, make_response, render_template, url_for, g, abort, session
from extensions import db, migrate, csrf, login_manager
from models import Admin, User
import secrets
from werkzeug.security import generate_password_hash
from flask_login import current_user

app = Flask(__name__)

# any env variable starts with flask_<name> add to config
# app.config.from_prefixed_env()

foo = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = foo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_SESSION_FOR_NEXT'] = True

with app.app_context():
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    db.create_all()

    admin = Admin.query.first()

    if not admin:
        passhash = generate_password_hash('admin')
        user = User(username='admin', email="admin@admin.com", password=passhash, is_admin=True)
        admin = Admin()
        user.admin = admin
        db.session.add(user)
        db.session.commit()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'You need to login first'
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = 'You need to re-login first'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

from auth.auth import auth as auth_blueprint
from admin.admin import admin as admin_blueprint
from brand.brand import brand as brand_blueprint
from influencer.influencer import influencer as influencer_blueprint
from errors.handlers import errors

app.register_blueprint(auth_blueprint, url_prefix='/')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(influencer_blueprint, url_prefix='/influencer')
app.register_blueprint(brand_blueprint, url_prefix='/brand')
app.register_blueprint(errors)

app.app_context().push()

# @app.before_request
# def before_request():
#     g.user = None
#     print(session)
#     if 'user' in session:
#         g.user = current_user

# @app.route('/set-cookie')
# def set_cookie():
#     resp = make_response(render_template('base.html'))
#     resp.set_cookie('foo', 'bar')
#     return resp

# @app.route('/cookies')
# def all_cookies():
#     cookies = request.cookies
#     print(cookies)
#     return render_template('base.html')


@app.route('/', methods=['GET'])
def home():
    username = None
    return render_template('home.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
