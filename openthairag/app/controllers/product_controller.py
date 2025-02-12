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
    
UPLOAD_FOLDER = "uploads/"  # Folder to store images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

mongo=Connection('otg_db')

def save_base64_image(base64_str, filename):
    image_data = base64.b64decode(base64_str.split(",")[-1])
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, "wb") as f:
        f.write(image_data)
    
    return file_path

def product_post(data):    
    image_paths = []
    
    if "pictures" in data and isinstance(data["pictures"], list):
        for idx, base64_img in enumerate(data["pictures"]):
            if base64_img.startswith("data:image"):
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{idx}.png"
                image_paths.append(save_base64_image(base64_img, filename))

    result = mongo.products.insert_one({
        "name": data.get("name"),
        "detail": data.get("detail"),
        "category": data.get("category"),
        "picture": image_paths,
        "created_at": datetime.utcnow()
    })

    return jsonify({
        "message": "Product inserted successfully",
        "id": str(result.inserted_id),
    }), 201

def product_patch(data):
    image_paths = []

    if "id" not in data:
        return jsonify({
            "message": "Data updated successfully",
        }), 400
    
    product = mongo.products.find_one({'_id': ObjectId(data['id'])})

    if "pictures" in data and isinstance(data["pictures"], list):
        for idx, base64_img in enumerate(data["pictures"]):
            if base64_img.startswith("data:image"):
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{idx}.png"
                image_paths.append(save_base64_image(base64_img, filename))
            else:
                image_paths.append(base64_img)
        product['picture'] = image_paths

    print("DDDD :",data['pictures'])
    print("Picture :",product['picture'])
    if "name" in data:
        product['name'] = data['name']

    if "detail" in data:
        product['detail'] = data['detail']

    if "category" in data:
        product['category'] = data['category']

    mongo.products.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            "name": product['name'],
            "detail": product['detail'],
            "category": product['category'],
            "picture": product['picture'],
            "created_at": datetime.now()
        }
    })

    return jsonify({
        "message": "Data updated successfully",
    }), 200

def product_get():
    data = mongo.products.find()
    resp = [
        {
            "id": str(item["_id"]),
            "name": item["name"],
            "detail": item["detail"],
            "category": item["category"],
            "pictures": item["picture"],
        } for item in data
    ]

    return jsonify({
        "data": resp,
    }), 200

def product_detail(id):
    data = mongo.products.find_one({'_id': ObjectId(id)})
    resp = {
            "id": str(data["_id"]),
            "name": data["name"],
            "detail": data["detail"],
            "category": data["category"],
            "pictures": data["picture"],
        }
    
    return jsonify({
        "data": resp,
    }), 200

def product_delete(doc_id):
    mongo.products.delete_one({'_id': ObjectId(doc_id)})
    return jsonify({
        "message": "Data remove successfully",
    }), 200
