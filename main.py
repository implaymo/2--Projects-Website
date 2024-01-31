from flask import Flask, render_template, request, redirect, url_for, flash
from forms import Login, SignUp
from database import db, User
from flask_login import LoginManager, login_user
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = os.getenv("SECRET_KEY")


with app.app_context():
    db.init_app(app) 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template('index.html')

@app.route("/generic")
def generic():
    return render_template('generic.html')

@app.route("/elements")
def elements():
    return render_template('elements.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.get_user_by_credentials(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash('You were successfully logged in')
            return redirect(url_for("home"))
        elif not user:
            flash("User not found. Sign up first!")
            return redirect(url_for("signup"))
        else:
            flash("Invalid credentials")
    else:
        flash("Form validation failed", 'danger')
    return render_template('login.html', form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUp()
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
        
    return render_template('signup.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)