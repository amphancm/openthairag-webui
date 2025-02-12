from .auth_routes import auth_bp
from .chat_routes import chat_bp
from .document_milvas_routes import document_system_bp
from .document_routes import document_bp
from .setting_routes import setting_bp
from .user_routes import account_bp
from .product_routes import product_bp
from .issue_routes import issue_bp

def register_routes(app):
    app.register_blueprint(auth_bp, name='auth', url_prefix="/auth")
    app.register_blueprint(chat_bp, name='chat', url_prefix="/chat")
    app.register_blueprint(document_system_bp, url_prefix="/document_sys")
    app.register_blueprint(document_bp, url_prefix="/document")
    app.register_blueprint(setting_bp, url_prefix="/setting")
    app.register_blueprint(account_bp, url_prefix="/user")
    app.register_blueprint(product_bp, url_prefix="/product")
    app.register_blueprint(issue_bp, url_prefix="/issue")