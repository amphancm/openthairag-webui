from json import dumps
from venv import logger
from flask import request, jsonify
from processing import collection
from bson import ObjectId
from utils import indexing
from db import Connection

mongo=Connection('otg_db')

def document_post(data):
    indexing_result = indexing(data['content'])
    
    result = mongo.docs.insert_one({
        'title':data['title'],
        'content':data['content'],
        'doc_id':str(indexing_result),
    })

    return dumps({
        "message": "Data inserted successfully", 
        "indexing_id": indexing_result,
        "id": str(result.inserted_id) 
    }), 201

def document_patch(data):
    delete_result = collection.delete(expr=f"id == {data['doc_id']}")
    logger.info(f"Delete result: {delete_result}")
    indexing_result = indexing(data['content'])

    mongo.docs.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            'title': data['title'],
            'content': data['content'],
            'doc_id': str(indexing_result)
        }
    })

    return jsonify({
        "message": "Data updated successfully",
        "indexing_id": str(indexing_result)
    }), 201

def document_get():
    data = mongo.docs.find()
    logger.info(f"Result result: {data}")
    resp = [
        {
            "id": str(item["_id"]),
            "title": item["title"],
            "content": item["content"],
            "doc_id": str(item["doc_id"])
        }
        for item in data
    ]
    return dumps(resp), 200

def delete_document(id):
    try:
        collection.load()

        result = mongo.docs.find_one({'_id': ObjectId(id)})
        delete_result = collection.delete(expr=f"id == {result['doc_id']}")
        message = f"Document with id {result['doc_id']} deleted successfully"
        
        logger.info(f"Delete result: {delete_result}")

        collection.flush()
        delete_result = mongo.docs.delete_one({'_id': ObjectId(id)})

        return jsonify({
            "message": message,
            "num_deleted": delete_result
        }), 200

    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        return jsonify({"error": str(e)}), 500