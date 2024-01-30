from flask import Flask, render_template, request, redirect, url_for
from forms import Login, SignUp
from database import db, User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

with app.app_context():
    db.init_app(app) 

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