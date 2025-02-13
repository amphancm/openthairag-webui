from flask import Flask, send_from_directory
from routes import register_routes
from config import Config
from flask_cors import CORS
import logging, os
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
from controllers.auth_controller import blacklist
from werkzeug.security import generate_password_hash

from db import Connection

logger = logging.getLogger(__name__)

MILVUS_HOST = os.environ.get('MILVUS_HOST', 'milvus')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')
VLLM_HOST = os.environ.get('VLLM_HOST', '172.17.0.1:8000')

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
register_routes(app)

mongo=Connection('otg_db')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

def create_default_user():
    default_username = "admin"
    default_email = "admin@admin.com"
    default_password = "admin"

    user = mongo.accounts.count_documents({"username": default_username})
    
    if not user:
        encrypted_password = generate_password_hash(default_password)

        mongo.accounts.insert_one({
            "username": default_username,
            "email": default_email,
            "role": "administrator",
            "password": encrypted_password,
        })
        logger.info("Default user created.")
    else:
        logger.info("Default user already exists.")

    if mongo.systemPrompt.count_documents({}) == 0:
        mongo.systemPrompt.insert_one({
            "content":"",
            "temperature":"",
        })
        logger.info("Default system Prompt created.")
    else:
        logger.info("Default system Prompt already exists.")

    if mongo.setting.count_documents({}) == 0:
        mongo.setting.insert_one({
            "time_activate": True,
            "line_activate": False,
            "fb_activate": False,
            "product_activate": False,
            "feedback_activate": False,
            "greeting_activate": False,
            "line_key": "",
            "line_secret": "",
            "facebook_token": "",
            "facebook_verify_password": "",
            "greeting_prompt": "",
        })
        logger.info("Default system setting created.")
    else:
        logger.info("Default system setting already exists.")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

create_default_user()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)