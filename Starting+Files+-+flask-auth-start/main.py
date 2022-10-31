from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from pymongo_insert import enter_customer, get_customers

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        #Log in and authenticate user after adding details to database.
        login_user(new_user)
        
        return redirect(url_for("secrets"))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        #Find user by email entered.
        user = User.query.filter_by(email=email).first()
        
        #Check stored password hash against entered password hashed.
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))
          
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    
    display_data = get_customers() #this should give you a list of dictionaries
    print(display_data)
    return render_template("secrets.html", name=current_user.name,current_list_customers=display_data)


@app.route('/new_customers', methods=["GET", "POST"])
@login_required
def new_customer():
    if request.method == "POST":
        customer_dict ={
            "cus_name" : request.form.get("Customer Name"),
            "meas_taken" : request.form.get("measurements taken?"),
            "adrs" : request.form.get("Address"),
            "phnumber" : request.form.get("Phone Number"),
            "email" : request.form.get("email")
        }
        
        enter_customer(customer_dict)
        #TODO want to redirect to current list of customers
        return redirect(url_for('new_customer'))
    return render_template("new_customer.html", name=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



    return send_from_directory('static', filename="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)