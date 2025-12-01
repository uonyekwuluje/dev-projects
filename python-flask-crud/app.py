from flask import Flask, render_template, request, redirect, url_for
from models import db, Item
from api import api
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql://pgadmin:password@localhost/cruddb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api, url_prefix="/api")


# --- Web UI (same as before) ----

@app.route("/")
def index():
    search = request.args.get("search", "")
    page = int(request.args.get("page", 1))
    per_page = 5

    query = Item.query
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("index.html", items=pagination.items,
                           page=page, pages=pagination.pages,
                           search=search)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        item = Item(
            name=request.form["name"],
            description=request.form["description"]
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", item=item)


@app.route("/delete/<int:id>")
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
