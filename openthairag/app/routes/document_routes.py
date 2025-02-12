from flask import Blueprint, request, jsonify
from controllers.document_controller import document_post, document_get, document_patch, delete_document
from flask_jwt_extended import jwt_required

document_bp = Blueprint("document", __name__)

@document_bp.route("", methods=["GET", "POST", "PATCH"])
@jwt_required()
def create_doc():
    if request.method == 'GET':
        return document_get()
    if request.method == 'POST':
        return document_post(request.json)
    if request.method == 'PATCH':
        return document_patch(request.json)

@document_bp.route("/<doc_id>", methods=["DELETE"])
@jwt_required()
def delete_doc(doc_id):
    return delete_document(doc_id)