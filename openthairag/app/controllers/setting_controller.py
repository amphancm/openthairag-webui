from db import Connection
from flask import Flask, request, jsonify
from bson import ObjectId
from bson.json_util import dumps

mongo=Connection('otg_db')

def setting_post(data):
    result = mongo.setting.insert_one(data)
    return jsonify({
        "message": "Data inserted successfully", 
        "id": str(result.inserted_id) 
    }), 201
    
def setting_patch(data):
    result = mongo.setting.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            'line_activate': data['line_activate'],
            'fb_activate': data['fb_activate'],
            'product_activate': data['product_activate'],
            'order_activate': data['order_activate'],
            'greeting_activate': data['greeting_activate'],
            'line_key': data['line_key'],
            'line_secret': data['line_secret'],
            'facebook_token': data['facebook_token'],
            'facebook_verify_password': data['facebook_verify_password'],
            'greeting_prompt': data['greeting_prompt']
        }
    })
    return jsonify({
        "message": "Data updated successfully", 
    }), 201

def setting_get():
    data = mongo.setting.find()
    return dumps(data), 200

def system_prompt_post(data):
    result = mongo.systemPrompt.insert_one(data)
    return jsonify({
        "message": "Data inserted successfully", 
        "id": str(result.inserted_id) 
    }), 201

def system_prompt_patch(data):
    result = mongo.systemPrompt.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            'content': data['content'] if 'content' in data else '',
            'temperature': data['temperature'] if 'temperature' in data else 0.4,
        }
    })
    return jsonify({
        "message": "Data updated successfully", 
    }), 201

def system_prompt_get():
    data = mongo.systemPrompt.find_one()
    return dumps(data), 200
