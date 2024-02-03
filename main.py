from flask import Flask, render_template, request, redirect, url_for, flash
from forms import Login, SignUp, Edit
from database import db, User, Post
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt 
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


bcrypt = Bcrypt(app) 

with app.app_context():
    db.init_app(app) 


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            error = "User not allowed to see that page."
            return render_template('index.html', current_user=current_user, error=error)
        return func(*args, **kwargs)
    return wrapper



login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["POST", "GET"])
def home():
    all_posts = Post.query.all()
    return render_template('index.html', current_user=current_user, all_posts=all_posts)

@app.route("/generic")
def generic():
    return render_template('generic.html', current_user=current_user)

@app.route("/elements")
@admin_required
def elements():
    return render_template('elements.html', current_user=current_user)

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    form = Login()
    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(username=form.username.data).one()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login with success!")
                return redirect(url_for("home"))
            else:
                error = "Wrong credentials. Try again!"
                return render_template('login.html', form=form, error=error)
        except Exception as e:
            error = f"There was an error: {e}"
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form, error=error)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUp()
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
            )
        hashed_password = bcrypt.generate_password_hash(user.password).decode('utf-8')
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
        
    return render_template('signup.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/edit/<int:post_id>", methods=["POST", "GET"])
@admin_required
def edit(post_id): 
    ### search the post that want to edit
    try: 
        searched_post = Post.query.get(post_id)
        ## populate the form with the content of searched_post
        form = Edit(
            title=searched_post.title,
            content=searched_post.content
        )
    except Exception as e:
        print(f"Error: {e}")

    if form.validate_on_submit():
        searched_post.title = form.title.data
        searched_post.content = form.content.data
        searched_post.image = form.image.data
        db.session.commit()

        return redirect(url_for("home"))
    
    return render_template("edit.html", form=form, post_id=searched_post.id) 


if __name__ == "__main__":
    app.run(debug=True)