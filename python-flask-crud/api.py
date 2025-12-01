from flask import Blueprint, request, jsonify
from models import db, Item

api = Blueprint("api", __name__)

# GET /api/items?search=abc&page=1&per_page=5
@api.route("/items", methods=["GET"])
def get_items():
    search = request.args.get("search", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    query = Item.query
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [
        {"id": i.id, "name": i.name, "description": i.description}
        for i in pagination.items
    ]

    return jsonify({
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    })


# POST /api/items
@api.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(name=data["name"], description=data.get("description", ""))
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item created", "id": item.id}), 201


# PUT /api/items/<id>
@api.route("/items/<int:id>", methods=["PUT"])
def update_item(id):
    data = request.get_json()
    item = Item.query.get_or_404(id)
    item.name = data["name"]
    item.description = data.get("description", "")
    db.session.commit()
    return jsonify({"message": "Item updated"})


# DELETE /api/items/<id>
@api.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})
