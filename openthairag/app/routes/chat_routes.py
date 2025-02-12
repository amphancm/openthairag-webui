from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.chat_controller import room_fb_option_get 
from controllers.chat_controller import room_fb_option_patch 
from controllers.chat_controller import room_fb_option_by_id_get
from controllers.chat_controller import room_fb_option_by_id_patch
from controllers.chat_controller import room_fb_option_by_id_delete 
from controllers.chat_controller import room_line_option_by_id_get 
from controllers.chat_controller import room_line_option_by_id_patch 
from controllers.chat_controller import room_line_option_by_id_delete 
from controllers.chat_controller import room_line_option_get 
from controllers.chat_controller import room_line_option_patch 
from controllers.chat_controller import room_option_post 
from controllers.chat_controller import room_option_patch 
from controllers.chat_controller import room_option_get
from controllers.chat_controller import room_option_by_id_delete
from controllers.chat_controller import room_option_by_id_get
from controllers.chat_controller import system_history_post 
from controllers.chat_controller import system_history_get 
from controllers.chat_controller import sending_line_assistant 
from controllers.chat_controller import sending_fb_assistant 
from controllers.chat_controller import message_submit_initial
from controllers.chat_controller import callback
from controllers.chat_controller import line_callback
from controllers.chat_controller import fb_callback_post
from controllers.chat_controller import fb_callback_get
from controllers.chat_controller import fbshortpollingMessage
from controllers.chat_controller import shortpollingMessage
from controllers.chat_controller import resetLineMessage
from controllers.chat_controller import resetFBMessage

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/room_fb_option", methods=['GET','PATCH'])
@jwt_required()
def room_fb_option_route():
    if request.method == 'GET':
        return room_fb_option_get()
    elif request.method == 'PATCH':
        return room_fb_option_patch(request.json)

@chat_bp.route("/room_fb_option/<id>", methods=['GET', 'DELETE', 'PATCH'])
@jwt_required()
def room_fb_option_by_id_route(id):
    if request.method == 'GET':
        return room_fb_option_by_id_get(id)
    elif request.method == 'PATCH':
        return room_fb_option_by_id_patch(request.json,id)
    elif request.method == 'DELETE':
        return room_fb_option_by_id_delete(id)

@chat_bp.route("/room_line_option", methods=['GET','PATCH'])
@jwt_required()
def room_line_option_route():
    if request.method == 'GET':
        return room_line_option_get()
    if request.method == 'PATCH':
        return room_line_option_patch(request.json)

@chat_bp.route("/room_line_option/<id>", methods=['GET', 'DELETE', 'PATCH'])
@jwt_required()
def room_line_option_by_id_route(id):
    if request.method == 'GET':
        return room_line_option_by_id_get(id)
    if request.method == 'PATCH':
        return room_line_option_by_id_patch(request.json)
    if request.method == 'DELETE':
        return room_line_option_by_id_delete(id)

@chat_bp.route("/room_option", methods=['POST', 'GET','PATCH'])
@jwt_required()
def room_option_route():
    if request.method == 'POST':
        return room_option_post(request.json)
    if request.method == 'PATCH':
        return room_option_patch(request.json)
    if request.method == 'GET':
        return room_option_get(request.args)

@chat_bp.route("/room_option/<id>", methods=['GET', 'DELETE'])
@jwt_required()
def room_option_by_id_route(id):
    if request.method == 'DELETE':
        return room_option_by_id_delete(id)
    if request.method == 'POST':
        return room_option_by_id_get(request.json, id)

@chat_bp.route("/chat_history", methods=['POST', 'GET','PATCH'])
@jwt_required()
def system_history_route():
    if request.method == 'POST':
        return system_history_post(request.json)
    if request.method == 'GET':
        return system_history_get(request.json)

@chat_bp.route("/sending_line_assistant", methods=['POST'])
@jwt_required()
def sending_line_assistant_route():
    return sending_line_assistant(request.json)

@chat_bp.route("/sending_fb_assistant", methods=['POST'])
@jwt_required()
def sending_fb_assistant_route():
    return sending_fb_assistant(request.json)

@chat_bp.route("/message_submit_initial/", methods=['POST','GET'])
@jwt_required()
def message_submit_initial_route():
    return message_submit_initial(request.json)

@chat_bp.route("/callback", methods=['POST'])
def callback_route():
    return callback(request.json)

@chat_bp.route("/line_callback", methods=['POST'])
def line_callback_route():
    return line_callback(request.json)

@chat_bp.route("/fb_callback", methods=['POST', 'GET'])
def fb_callback_route():
    if request.method == 'POST':
        return fb_callback_post(request.json)
    if request.method == 'GET':
        return fb_callback_get(request.args)
    

@chat_bp.route("/fb_short_polling_message", methods=['GET'])
def fb_short_polling_message_route():
    if request.method == 'GET':
        return fbshortpollingMessage()

@chat_bp.route("/short_polling_message", methods=['GET'])
def short_polling_message_route():
    if request.method == 'GET':
        return shortpollingMessage()

@chat_bp.route('/reset_line_tempMessage', methods=['POST'])
def reset_line_message():
    return resetLineMessage(request.json)

@chat_bp.route('/reset_fb_tempMessage', methods=['POST'])
def reset_fb_message():
    return resetFBMessage(request.json)
    