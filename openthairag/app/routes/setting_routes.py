from flask import Blueprint, request, jsonify
from controllers.setting_controller import setting_get, setting_post, setting_patch, system_prompt_get, system_prompt_post, system_prompt_patch
from flask_jwt_extended import jwt_required

setting_bp = Blueprint("setting", __name__)

@setting_bp.route("/general", methods=['POST', 'PATCH', 'GET'])
@jwt_required()
def setting():
    if request.method == 'GET':
        return setting_get()
    if request.method == 'POST':
        return setting_post(request.json)
    if request.method == 'PATCH':
        return setting_patch(request.json)

@setting_bp.route("/system_prompt", methods=['POST', 'GET', 'PATCH'])
@jwt_required()
def system_prompt():
    if request.method == 'GET':
        return system_prompt_get()
    if request.method == 'POST':
        return system_prompt_post(request.json)
    if request.method == 'PATCH':
        return system_prompt_patch(request.json)
