from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user, fresh_login_required
from forms import LoginForm, RegisterForm
from models import User, Admin, Brand, Influencer, Profile
from extensions import  db
from constants import avatar


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        if current_user.is_influencer:
            return redirect(url_for('influencer.dashboard', infu_id=current_user.influencer.id))
        else:
            return redirect(url_for('brand.dashboard', brand_id=current_user.brand.id))
        
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                
                if 'next' in session:
                    next = session['next']
                    session.pop('next', None)
                    return redirect(next)

                if user.is_admin:
                    return redirect(url_for('admin.dashboard', admin=user.admin.id))
                elif user.is_influencer:
                    return redirect(url_for('influencer.dashboard', infu_id=user.influencer.id))
                else:
                    return redirect(url_for('brand.dashboard', brand_id=user.brand.id))
            else:
                flash('Invalid credentials', category='error')
        else:
            flash('Invalid credentials', category='error')

    if 'next' not in session and request.args.get('next'):
        session['next'] = request.args.get('next')

    return render_template('login.html', form=form, user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        industry = form.industry.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists', category='error')
        else:
            passhash = generate_password_hash(password)
            new_user = User(username=username, email=email, password=passhash)
            profile = Profile()
            profile.avatar = avatar.format(username)
            new_user.profile = profile

            if role.lower().strip() == 'influencer':
                new_user.is_influencer = True
                new_infu = Influencer(name=username.title(), industry=industry)
                new_user.influencer = new_infu
                flash('New influencer created', category='success')
            else:
                new_user.is_brand = True
                new_brand = Brand(name=username.title(), industry=industry)
                new_user.brand = new_brand
                flash('New brand created', category='success')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/fresh')
@fresh_login_required
def fresh():
    return '<h2>Fresh Page</h2>'
