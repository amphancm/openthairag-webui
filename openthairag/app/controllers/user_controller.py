from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from db import Connection
from flask import jsonify
from bson import ObjectId

mongo=Connection('otg_db')

def account_post(data):
    encrypted_password = generate_password_hash(data['password'])
    result = mongo.accounts.insert_one({
        'username': data['username'],
        'email': data['email'],
        'role': data['role'],
        'password': encrypted_password,
    })

    return dumps({
        "message": "Account created successfully", 
        "id": str(result.inserted_id) 
    }), 201
    
def account_patch(data):
    update_data = {
        'username': data['username'],
        'email': data['email'],
        'role': data['role'],
    }

    mongo.accounts.update_one({
        '_id': ObjectId(data['id'])
    }, {
        "$set": update_data
    })

    return jsonify({
        "message": "Account updated successfully",
    }), 200

def account_get():
    data = mongo.accounts.find()
    accounts = [
        {
            "id": str(account["_id"]),
            "username": account["username"],
            "email": account["email"],
            "role": account["role"],
        } for account in data
    ]
    return jsonify({
        "data": accounts
    }), 200

def account_get_by_detail(id):
    data = mongo.accounts.find_one({'_id': ObjectId(id)})
    accounts = {
        "id": str(data["_id"]),
        "username": data["username"],
        "email": data["email"],
        "role": data["role"],
    }
    
    return jsonify({
        "data": accounts
    }), 200

def account_delete(id):
    try:
        delete_result = mongo.accounts.delete_one({'_id': ObjectId(id)})
        if delete_result.deleted_count > 0:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def account_change_password(id, data):
    # Change password
    try:
        if 'password' in data:
            new_password = generate_password_hash(data['password'])

            update_result = mongo.accounts.update_one(
                {'_id': ObjectId(id)},
                {"$set": {'password': new_password}}
            )

            if update_result.modified_count > 0:
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                return jsonify({"error": "User not found or no change in password"}), 404
        else:
            return jsonify({"error": "Password is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
