from flask import Blueprint, request
from controllers.issue_controller import issue_get, issue_post, issue_patch, issue_delete, issue_detail
from flask_jwt_extended import jwt_required

issue_bp = Blueprint("issue", __name__)

@issue_bp.route("", methods=['POST', 'PATCH', 'GET'])
@jwt_required()
def setting():
    if request.method == 'GET':
        return issue_get()
    if request.method == 'POST':
        return issue_post(request.json)
    if request.method == 'PATCH':
        return issue_patch(request.json)

@issue_bp.route("/<id>", methods=['GET', 'DELETE'])
@jwt_required()
def issue_delete_route(id):
    if request.method == 'GET':
        return issue_detail(id)
    if request.method == 'DELETE':
        return issue_delete(id)
