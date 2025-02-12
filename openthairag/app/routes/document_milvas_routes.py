from flask import Blueprint, request, jsonify
from controllers.document_milvas_controller import index_text, delete_documents, list_documents
from flask_jwt_extended import jwt_required

document_system_bp = Blueprint("document_system", __name__)

@document_system_bp.route("/", methods=["GET"])
@jwt_required()
def list_docs_text():
    return index_text()

@document_system_bp.route("/delete/<doc_id>", methods=["DELETE"])
@jwt_required()
def indexing_doc(doc_id):
    return delete_documents(doc_id)

@document_system_bp.route("/list", methods=["GET"])
@jwt_required()
def list_docs():
    return list_documents()