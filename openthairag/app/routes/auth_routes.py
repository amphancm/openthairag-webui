from flask import Blueprint, request
from controllers.auth_controller import login, logout, profile
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/', methods=["GET"])
def index():
    return "This is an example app"

@auth_bp.route("/login", methods=["POST"])
def login_route():
    print('Login')
    return login(request.json)

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_route():
    return logout(get_jwt()["jti"])

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile_route():
    return profile(get_jwt_identity())