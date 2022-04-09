from typing import List, Callable, Optional, Tuple

from flask import jsonify, request, Request
from markupsafe import escape

from api import app, engine
from api.base_api import BaseApi
from service.authorize.authorize import Authorize
from src.product.product import Product
from src.product.product_repository import get_product_repository


class ProductsApi(BaseApi):
    def __init__(self, request: Request, methods: List[str]):
        super(ProductsApi, self).__init__(request=request, methods=methods)

        self.methods_map = {
            "get_products": self.get_products,
            "get_product_details": self.get_product_details,
            "create_product": self.create_product,
            "update_product": self.update_product
        }

    def execute(self, method_name: str, **kwargs):
        return self.methods_map[method_name](**kwargs)

    def get_products(self):
        product_repository = get_product_repository(engine)
        products = product_repository.get_all()
        data = [
            {
                "id": it.id,
                "name": it.name,
                "origin": it.country_of_origin,
                "calories": it.calories,
                "flavor": it.flavor
            }
            for it in products
        ]

        return self.respond(code=200, data=data)

    def get_product_details(self, product_id: str):
        product_repository = get_product_repository(engine)
        product = product_repository.get_by_id(_id=escape(product_id))
        if not product:
            return self.respond(code=404)

        data = {
            "id": product.id,
            "name": product.name,
            "origin": product.country_of_origin,
            "calories": product.calories,
            "flavor": product.flavor
        }

        return self.respond(code=200, data=data)

    def create_product(self):
        valid, message = self.authorizer.has_role(role="Seller")

        if not valid:
            return self.respond(code=403, message=message)

        request_json_body_data = self.request.get_json()
        required_parameters = ["name", "origin", "calories", "flavor"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        product_repository = get_product_repository(engine)
        name = request_json_body_data["name"]
        origin = request_json_body_data["origin"]
        calories = request_json_body_data["calories"]
        flavor = request_json_body_data["flavor"]

        product = Product(name=name, country_of_origin=origin, calories=calories, flavor=flavor)
        product_repository.insert(product)

        data = {
            "product_id": product.id
        }

        return self.respond(code=200, data=data)

    def update_product(self, product_id: str):
        valid, message = self.authorizer.has_role(role="Seller")

        if not valid:
            return self.respond(code=403, message=message)

        product_repository = get_product_repository(engine)
        product = product_repository.get_by_id(_id=escape(product_id))
        if not product:
            return self.respond(code=404)

        json_body_data = self.request.get_json()

        product_attrs = [key for key in product.to_dict()]
        for key, value in json_body_data.items():
            if key in product_attrs:
                setattr(product, key, value)
            elif key == "origin":
                setattr(product, "country_of_origin", value)

        product_repository.insert(product)

        data = {
            "id": product.id,
            "name": product.name,
            "origin": product.country_of_origin,
            "calories": product.calories,
            "flavor": product.flavor
        }

        return self.respond(code=200, data=data)


@app.route("/products", methods=["GET"])
def get_products():
    return ProductsApi(request=request, methods=["GET"]).execute(method_name="get_products")


@app.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id: str):
    return ProductsApi(request=request, methods=["GET"]).execute(method_name="get_product_details",
                                                                 product_id=product_id)


@app.route("/products", methods=["POST"])
def create_product():
    return ProductsApi(request=request, methods=["POST"]).execute(method_name="create_product")


@app.route("/products/<string:product_id>", methods=["PUT"])
def update_product(product_id: str):
    return ProductsApi(request=request, methods=["PUT"]).execute(method_name="update_product", product_id=product_id)
