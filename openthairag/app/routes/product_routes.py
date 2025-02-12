from flask import Blueprint, request
from controllers.product_controller import product_get, product_post, product_patch, product_delete, product_detail
from flask_jwt_extended import jwt_required

product_bp = Blueprint("product", __name__)

@product_bp.route("", methods=['POST', 'PATCH', 'GET'])
@jwt_required()
def setting():
    if request.method == 'GET':
        return product_get()
    if request.method == 'POST':
        return product_post(request.json)
    if request.method == 'PATCH':
        return product_patch(request.json)

@product_bp.route("/<id>", methods=['GET', 'DELETE'])
@jwt_required()
def product_delete_route(id):
    if request.method == 'GET':
        return product_detail(id)
    if request.method == 'DELETE':
        return product_delete(id)
