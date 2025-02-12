from flask import request, jsonify
from processing import collection
from utils import indexing
import logging

logger = logging.getLogger(__name__)

def index():
    return "Welcome to OTG Rag!", 200

def index_text():
    try:
        # Get text from request
        data = request.get_json()
        text = data.get("text")
        result = indexing(text)
        
        return jsonify({
            "message": "Text indexed successfully",
            "id": result
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_documents(doc_id):
    try:
        collection.load()
        if doc_id == '*':
            delete_result = collection.delete(expr="id >= 0")
            message = "All documents deleted successfully"
        else:
            delete_result = collection.delete(expr=f"id == {doc_id}")
            message = f"Document with id {doc_id} deleted successfully"
        
        logger.info(f"Delete result: {delete_result}")

        collection.flush()

        return jsonify({
            "message": message,
            "num_deleted": delete_result.delete_count
        }), 200

    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def list_documents():
    try:
        collection.load()
        # Get query parameters
        query = request.args.get('query', '')
        limit = min(int(request.args.get('limit', 10)), 16384)  # Default 10, max 16384
        offset = max(0, int(request.args.get('offset', 0)))  # Ensure non-negative offset

        # Ensure (offset + limit) is within Milvus range
        if offset + limit > 16384:
            limit = 16384 - offset

        # Prepare the search expression
        expr = f"text like '%{query}%'" if query else ""

        # Query entities in the collection
        results = collection.query(
            expr=expr,
            output_fields=["id", "text", "embedding"],
            offset=offset,
            limit=limit
        )
        
        # Prepare the response
        documents = [
            {
                "id": str(doc['id']),
                "text": doc['text'] + "...",
                "embedding": [float(x) for x in doc['embedding']]  # Convert to list of floats
            } for doc in results
        ]
        
        # Log the number of documents retrieved
        logger.info(f"Retrieved {len(documents)} documents")

        return jsonify({
            "message": "Documents retrieved successfully",
            "documents": documents,
            "total": len(documents),
            "offset": offset,
            "limit": limit
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500