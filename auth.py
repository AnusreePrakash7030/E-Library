from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dept = db.Column(db.String)
    coursecode = db.Column(db.String)
    Subject = db.Column(db.String)
    link = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("project.html")

# Login Page


@app.route("/loginproject", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            # Authentication successful
            return render_template("addmet.html")
        else:
            # Invalid username or password
            return render_template(
                "loginproject.html", error="Invalid username or password"
            )
    else:
        return render_template("loginproject.html")

# Add Materials Page


@app.route('/addmet', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['dept']
        coursecode = request.form['coursecode']
        Subject = request.form['Subject']
        link = request.form['link']

        new_user = User(name=name, dept=dept,
                        coursecode=coursecode, Subject=Subject, link=link)
        db.session.add(new_user)
        db.session.commit()
        return 'your data has been submitted'

    else:
        return render_template('addmet.html')

# Retreiving data


@app.route('/project', methods=['GET', 'POST'])
def search():
    result = []
    if request.method == 'POST':
        search_query = request.form['query']

        for user in User.query.all():
            if user.Subject == search_query:
                result.append(user.link)
        return render_template('data.html', result=result)
    else:
        return render_template("project.html")


@app.route('/data', methods=['GET', 'POST'])
def search1():
    result = []
    if request.method == 'POST':
        search_query = request.form['query']

        for user in User.query.all():
            if user.Subject == search_query:
                result.append(user.link)
        return render_template('data.html', result=result)
    else:
        return render_template("data.html")


if __name__ == "__main__":
    app.run(debug=True)
