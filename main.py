from flask import Flask, render_template, request, redirect, url_for, flash
from forms import Login, SignUp
from database import db, User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template('index.html', current_user=current_user)

@app.route("/generic")
def generic():
    return render_template('generic.html', current_user=current_user)

@app.route("/elements")
def elements():
    return render_template('elements.html', current_user=current_user)

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    form = Login()
    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(username=form.username.data).one()
            if user.password == form.password.data:
                login_user(user)
                flash("Login with success!")
                return redirect(url_for("home"))
            else:
                error = "Wrong credentials. Try again!"
                return redirect(url_for("signup"))
        except Exception as e:
            error = f"There was an error: {e}"
            return redirect(url_for("login"))
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)