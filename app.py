from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from forms import RegistrationForm,LoginForm
from models import User, Card, BagItem,Testimonial,Collection
from extensions import db, login_manager, bcrypt

# --- App & Config ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

@login_manager.user_loader 
def load_user(user_id): 
    return User.query.get(int(user_id)) 

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# --- Routes ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        existing = User.query.filter_by(email=register_form.email.data).first()
        if existing:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        hashed_pw = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('auth.html', login_form=login_form, register_form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login_form = LoginForm()
    register_form = RegistrationForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login unsuccessful. Check email and password.', 'auth')

    return render_template('auth.html', login_form=login_form, register_form=register_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    cards = Card.query.all()
    collections = Collection.query.all()
    testimonials = Testimonial.query.all()
    return render_template('home.html',
                           cards=cards,
                           collections=collections,
                           testimonials=testimonials)

# --- Footer Pages ---
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/how_to_order')
def how_to_order():
    return render_template('order_guide.html')

@app.route('/wedding_cards')
def wedding_cards():
    return render_template('wedding_cards.html')

@app.route('/hindu_wedding')
def hindu_wedding():
    return render_template('hindu_wedding.html')


@app.route('/card/<card_name>')
def card_details(card_name):
    return render_template('card_details.html', card_name=card_name)

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    title = request.form.get('card_title')
    image = request.form.get('image_url')
    price = request.form.get('price')

    if 'wishlist' not in session:
        session['wishlist'] = []

    wishlist = session['wishlist']

    for item in wishlist:
        if item['title'] == title:
            flash('Item already in wishlist.','wishlist')
            return redirect(url_for('wishlist'))

    wishlist.append({'title': title, 'image': image, 'price': price})
    session['wishlist'] = wishlist
    flash('Item added to wishlist!','wishlist')

    return redirect(url_for('wishlist'))

@app.route('/wishlist')
def wishlist():
    wishlist = session.get('wishlist', [])
    return render_template('wishlist.html', wishlist=wishlist)

@app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    title = request.form.get('card_title')

    wishlist = session.get('wishlist', [])
    wishlist = [item for item in wishlist if item['title'] != title]

    session['wishlist'] = wishlist
    flash(f'"{title}" removed from wishlist.','wishlist')

    return redirect(url_for('wishlist'))

# ✅ Buy Now: Add item to Bag
@app.route('/add_to_cart/<int:card_id>')
@login_required
def add_to_cart(card_id):
    item = BagItem(user_id=current_user.id, card_id=card_id, quantity=1)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('bag'))

# ✅ Show Bag Contents
@app.route('/bag')
@login_required
def bag():
    bag_items = BagItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.card.price * item.quantity for item in bag_items)
    return render_template('bag.html', bag_items=bag_items, total=total)
# ✅ Remove an Item
@app.route('/remove_from_bag/<int:item_id>', methods=['POST'])
@login_required
def remove_from_bag(item_id):
    item = BagItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('bag'))

@app.route('/checkout/<int:item_id>', methods=['POST'])
@login_required
def checkout(item_id):
    item = BagItem.query.get_or_404(item_id)
    # Store order, mark as purchased, etc. (You can expand this logic)
    return redirect(url_for('order_confirmed'))

@app.route('/order-confirmed')
@login_required
def order_confirmed():
    return render_template('order_confirmed.html')


def get_discount(code, subtotal):
    if code == 'MAR0057':  # Example coupon code
        return round(0.10 * subtotal, 2)  # 10% off
    return 0.0


@app.route('/payment')
@login_required
def payment_page():
    bag_items = BagItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.price * item.quantity for item in bag_items)

    shipping = 0.0  # Assuming free shipping
    coupon_code = session.get('coupon', '')
    discount = get_discount(coupon_code, subtotal)
    total = subtotal - discount

    return render_template('payment.html',
                           bag_items=bag_items,
                           subtotal=subtotal,
                           shipping=shipping,
                           coupon_code=coupon_code,
                           discount=discount,
                           total=total)

# --- Run ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
