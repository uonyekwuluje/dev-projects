from flask import Flask, render_template, request, redirect, url_for
from models import db, Item

app = Flask(__name__)

# Update with your actual database credentials
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://pgadmin:password@localhost/cruddb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create tables automatically
with app.app_context():
    db.create_all()


# --- READ ---
@app.route("/")
def index():
    items = Item.query.all()
    return render_template("index.html", items=items)


# --- CREATE ---
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")


# --- UPDATE ---
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", item=item)


# --- DELETE ---
@app.route("/delete/<int:id>")
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
