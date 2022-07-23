from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    present = db.Column(db.Boolean)
        

@app.route("/")
def home():
    guests = Guest.query.all()
    for guest in guests:
        print(guest.name)
    
    return render_template("base.html", guests=guests)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    newGuest = Guest(name=name, present=False)
    db.session.add(newGuest)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:guest_id>")
def delete(guest_id):
    guest = Guest.query.filter_by(id=guest_id).first()
    db.session.delete(guest)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:guest_id>")
def update(guest_id):
    guest = Guest.query.filter_by(id=guest_id).first()
    guest.present = not guest.present
    db.session.commit()
    return redirect(url_for("home"))





if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)