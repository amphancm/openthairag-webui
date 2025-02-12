from processing import generate_embedding, collection
from flask import jsonify
import numpy as np
import logging

logger = logging.getLogger(__name__)

def indexing(text):
    if not text:
        return jsonify({"error": "No text provided"}), 400

    embedding = generate_embedding(text).numpy().flatten().tolist()

    entity = {
        "text": text,
        "embedding": embedding
    }

    logger.info("Indexing new document:")
    logger.debug(f"Text: {text[:100]}...")
    logger.debug(f"Embedding shape: {np.array(embedding).shape}")
    logger.debug(f"Embedding sample: {embedding[:5]}...") 
    logger.debug(f"Full entity: {entity}")

    insert_result = collection.insert([entity])

    logger.info(f"Insert result: {insert_result}")

    collection.flush()

    return insert_result.primary_keys[0]