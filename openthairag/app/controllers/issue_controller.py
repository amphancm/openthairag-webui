from json import dumps
from venv import logger
from flask import request, jsonify
from processing import collection
from bson import ObjectId
from utils import indexing
from db import Connection
from datetime import datetime
import os
import base64

mongo=Connection('otg_db')

def issue_post(data):    
    result = mongo.issues.insert_one({
        "name": data.get("name"),
        "detail": data.get("detail"),
        "user_name":  data.get("user_name"),
        "created_at": datetime.utcnow()
    })

    return jsonify({
        "message": "Product inserted successfully",
        "id": str(result.inserted_id),
    }), 201

def issue_patch(data):
    if "id" not in data:
        return jsonify({
            "message": "issue need id",
        }), 400
    
    issue = mongo.issues.find_one({'_id': ObjectId(data['id'])})

    if "name" in data:
        issue['name'] = data['name']

    if "detail" in data:
        issue['detail'] = data['detail']

    if "user_name" in data:
        issue['user_name'] = data['user_name']

    mongo.issues.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            "name": issue["name"],
            "detail": issue["detail"],
            "user_name":  issue["user_name"],
            "created_at": datetime.now()
        }
    })

    return jsonify({
        "message": "Data updated successfully",
    }), 200

def issue_get():
    data = mongo.issues.find()
    resp = [
        {
            "id": str(item["_id"]),
            "name": item["name"],
            "detail": item["detail"],
            "user_name": item["user_name"],
        } for item in data
    ]

    return jsonify({
        "data": resp,
    }), 200

def issue_detail(id):
    data = mongo.issues.find_one({'_id': ObjectId(id)})
    if(not data):
        return jsonify({
            "message": "cannot found this id",
        }), 400
    
    print("data :",data)
    resp = {
        "id": str(data["_id"]),
        "name": data["name"],
        "detail": data["detail"],
        "user_name": data["user_name"],
    }
    
    return jsonify({
        "data": resp,
    }), 200

def issue_delete(doc_id):
    delete_result = mongo.issues.delete_one({'_id': ObjectId(doc_id)})
    return jsonify({
        "deleted_count": delete_result.deleted_count,
        "message": "Data remove successfully",
    }), 200
