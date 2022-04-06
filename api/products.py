from flask import jsonify, request
from markupsafe import escape

from api import app, engine
from src.product.product import Product
from src.product.product_repository import get_product_repository


@app.route("/products", methods=["GET"])
def get_products():
    product_repository = get_product_repository(engine)
    products = product_repository.get_all()
    return jsonify([
        {
            "id": it.id,
            "name": it.name,
            "origin": it.country_of_origin,
            "calories": it.calories,
            "flavor": it.flavor
        }
        for it in products
    ])


@app.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    product_repository = get_product_repository(engine)
    product = product_repository.get_by_id(_id=escape(product_id))
    if not product:
        return {}

    return {
        "id": product.id,
        "name": product.name,
        "origin": product.country_of_origin,
        "calories": product.calories,
        "flavor": product.flavor
    }


@app.route("/products", methods=["POST"])
def create_product():
    json_body_data = request.get_json()
    # TODO: Refactor required parameters logic.
    # TODO: Return error status code.
    if "name" not in json_body_data or not json_body_data["name"]:
        return {
            "success": False,
            "message": "name is required"
        }

    if "origin" not in json_body_data or not json_body_data["origin"]:
        return {
            "success": False,
            "message": "origin is required"
        }

    if "calories" not in json_body_data or not json_body_data["calories"]:
        return {
            "success": False,
            "message": "calories is required"
        }

    if "flavor" not in json_body_data or not json_body_data["flavor"]:
        return {
            "success": False,
            "message": "flavor is required"
        }

    product_repository = get_product_repository(engine)
    name = json_body_data["name"]
    origin = json_body_data["origin"]
    calories = json_body_data["calories"]
    flavor = json_body_data["flavor"]

    product = Product(name=name, country_of_origin=origin, calories=calories, flavor=flavor)
    product_repository.insert(product)

    return {
        "product_id": product.id
    }


@app.route("/products/<product_id>", methods=["PUT"])
def update_products(product_id):
    product_repository = get_product_repository(engine)
    product = product_repository.get_by_id(_id=escape(product_id))
    if not product:
        return {}

    json_body_data = request.get_json()

    product_attrs = [key for key in product.to_dict()]
    for key, value in json_body_data.items():
        if key in product_attrs:
            setattr(product, key, value)
        elif key == "origin":
            setattr(product, "country_of_origin", value)
            
    product_repository.insert(product)

    return {
        "id": product.id,
        "name": product.name,
        "origin": product.country_of_origin,
        "calories": product.calories,
        "flavor": product.flavor
    }
