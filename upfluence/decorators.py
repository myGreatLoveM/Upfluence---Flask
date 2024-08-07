from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def brand_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user and not current_user.is_brand:
            return redirect(url_for('auth.logout'))
        if (kwargs['brand_id'] != current_user.brand.id):
            return redirect(url_for('auth.logout'))
        return func(*args, **kwargs)
    return inner


def influencer_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user and not current_user.is_influencer:
            return redirect(url_for('auth.logout'))
        if (kwargs['infu_id'] != current_user.influencer.id):
            return redirect(url_for('auth.logout'))
        return func(*args, **kwargs)
    return inner


# def auth_required(func):
#     @wraps(func)
#     def inner(*args, **kwargs):
#         if 'user_id' in session:
#             return func(*args, **kwargs)
#         flash('Please login to continue')
#         return redirect(url_for('login'))
#     return inner


# def admin_required(func):
#     @wraps(func)
#     def inner(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('Please login to continue')
#             return redirect(url_for('login'))
#         user = User.query.get(session['user_id'])
#         if user.is_admin:
#             return func(*args, **kwargs)
#         flash('You are not authorized to access')
#         return redirect(url_for('home'))
#     return inner
