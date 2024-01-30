from flask import Flask, render_template
from forms import Login, SignUp
from database import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


with app.app_context():
    db.init_app(app)
    db.create_all()
    

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
    return render_template('signup.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)