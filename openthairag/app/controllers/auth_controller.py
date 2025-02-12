from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, unset_jwt_cookies, get_jwt
from datetime import timedelta
from flask import jsonify
from bson import ObjectId
import logging
from db import Connection

mongo=Connection('otg_db')

blacklist = set()
logger = logging.getLogger(__name__)

def login(data):
    username = data.get("username")
    password = data.get("password")
    remember = data.get("remember", False) 

    print(f"user result: {username} {password} {remember}")
    
    user = mongo.accounts.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        expiration = timedelta(days=7) if remember else timedelta(hours=1)  
        access_token = create_access_token(
            identity={"id": str(user["_id"]), "username": username},
            expires_delta=expiration
        )
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    return jsonify({"message": "Invalid username or password"}), 401

def logout(jti):
    blacklist.add(jti)  
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    response = jsonify({"message": "Logout successful"})
    return response, 200

def profile(identity):
    user_id = identity.get("id")
    user = mongo.accounts.find_one({'_id': ObjectId(user_id)})

    logger.info(f"user result: {user}")
    if user:
        return jsonify({
            "username": user["username"],
            "email": user.get("email")
        }), 200
    
    return jsonify({"message": "User not found"}), 400