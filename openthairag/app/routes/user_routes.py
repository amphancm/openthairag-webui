from flask import Blueprint, request
from controllers.user_controller import account_get, account_post, account_patch, account_delete, account_change_password, account_get_by_detail
from flask_jwt_extended import jwt_required

account_bp = Blueprint("account", __name__)

@account_bp.route("", methods=['POST', 'PATCH', 'GET'])
@jwt_required()
def setting():
    if request.method == 'GET':
        return account_get()
    if request.method == 'POST':
        return account_post(request.json)
    if request.method == 'PATCH':
        return account_patch(request.json)

@account_bp.route("/<id>", methods=['DELETE', 'GET'])
@jwt_required()
def account_operation_route(id):
    if request.method == 'GET':
        return account_get_by_detail(id)
    if request.method == 'DELETE':
        return account_delete(id)


@account_bp.route("/password/<id>", methods=['PATCH'])
@jwt_required()
def account_change_password_route(id):
    return account_change_password(id, request.json)
