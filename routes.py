# from flask import render_template, redirect, url_for, flash, request
# from app import app
# from models import User
# from extensions import db
# from forms import RegistrationForm, LoginForm
# from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))

#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_pw = generate_password_hash(form.password.data)
#         user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
#         db.session.add(user)
#         db.session.commit()
#         flash('Account created! You can now log in.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and check_password_hash(user.password, form.password.data):
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash('Login unsuccessful. Check email and password.', 'danger')
#     return render_template('login.html', form=form)
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
# @app.route('/home')
# @login_required
# def home():
#     return render_template('home.html')


# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/faq')
# def faq():
#     return render_template('faq.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/how_to_order')
# def how_to_order():
#     return render_template('order_guide.html')

# @app.route('/wedding_cards')
# def wedding_cards():
#     return render_template('wedding_cards.html')

# @app.route('/hindu_wedding')
# def hindu_wedding():
#     return render_template('hindu_wedding.html')