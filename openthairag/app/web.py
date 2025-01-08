from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import numpy as np
import logging
from db import Connection
from bson.json_util import dumps
from bson import ObjectId
from processing import compute_model,generate_embedding,rerank_documents, collection

from linebot.models import *
from linebot import *
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, unset_jwt_cookies, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
import socketio

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
logger = logging.getLogger(__name__)
blacklist = set()

logger.info("Logger initialized for Flask application")

MILVUS_HOST = os.environ.get('MILVUS_HOST', 'milvus')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')
VLLM_HOST = os.environ.get('VLLM_HOST', '172.17.0.1:8000')

app = Flask(__name__)
CORS(app)
logger.info("Successfully Setup Flask Web Service.")
# ws = create_connection("ws://websocket-server:3000") # Update host/port if running Docker
sio = socketio.Client()
sio.connect('http://websocket-server:3000')

# JWT secret key
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

mongo=Connection('otg_db')

# Flask route for index page
@app.route("/", methods=["GET"])
def index():
    return "Welcome to OpenThaiRAG!", 200

# Flask route for indexing text
@app.route("/index", methods=["POST"])
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

# Flask route for deleting indexed documents
@app.route("/delete/<doc_id>", methods=["DELETE"])
def delete_documents(doc_id):
    try:
        collection.load()
        if doc_id == '*':
            # Delete all entities in the collection
            delete_result = collection.delete(expr="id >= 0")
            message = "All documents deleted successfully"
        else:
            # Delete specific document
            delete_result = collection.delete(expr=f"id == {doc_id}")
            message = f"Document with id {doc_id} deleted successfully"
        
        # Log the delete result
        logger.info(f"Delete result: {delete_result}")

        # Ensure the changes are immediately reflected
        collection.flush()

        return jsonify({
            "message": message,
            "num_deleted": delete_result.delete_count
        }), 200

    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Flask route for listing indexed documents
@app.route("/list", methods=["GET"])
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
        logger.error(f"Error listing documents: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/system_prompt", methods=['POST', 'GET', 'PATCH'])
def system_prompt():
    if request.method == 'POST':
        data = request.json
        result = mongo.systemPrompt.insert_one(data)
        return jsonify({
            "message": "Data inserted successfully", 
            "id": str(result.inserted_id) 
        }), 201
    
    elif request.method == 'PATCH':
        data = request.json
        result = mongo.systemPrompt.update_one({
            '_id': ObjectId(data['id'])
        },
        {
            "$set":{
                'content': data['content'],
                'temperature': data['temperature'],
                'greeting': data['greeting']
            }
        })
        return jsonify({
            "message": "Data updated successfully", 
        }), 201

    elif request.method == 'GET':
        data = mongo.systemPrompt.find()
        return dumps(data), 200

@app.route("/setting", methods=['POST', 'GET', 'PATCH'])
def setting():
    if request.method == 'POST':
        data = request.json
        result = mongo.setting.insert_one(data)
        return jsonify({
            "message": "Data inserted successfully", 
            "id": str(result.inserted_id) 
        }), 201
    
    elif request.method == 'PATCH':
        data = request.json
        result = mongo.setting.update_one({
            '_id': ObjectId(data['id'])
        },
        {
            "$set":{
                'line_key': data['line_key'],
                'line_secret': data['line_secret']
            }
        })
        return jsonify({
            "message": "Data updated successfully", 
        }), 201

    elif request.method == 'GET':
        data = mongo.setting.find()
        return dumps(data), 200

@app.route("/document", methods=['POST', 'GET', 'PATCH', 'DELETE'])
def docs_list():
    if request.method == 'POST':
        data = request.json
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

    elif request.method == 'PATCH':
        data = request.json
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

    elif request.method == 'GET':
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

@app.route("/document/<id>", methods=['GET', 'DELETE'])
def docs_detail(id):

    if request.method == 'DELETE':
        result = mongo.docs.find({'_id': ObjectId(id)})
        print(f'result : {result[0]}')
        
        delete_result = collection.delete(expr=f"id == {result[0]['doc_id']}")
        logger.info(f"Delete result: {delete_result}")
        
        mongo.docs.delete_one({'_id': ObjectId(id)})

        return jsonify({
            "message": "Data Delete successfully",
        }), 201

    elif request.method == 'GET':
        result = mongo.docs.find({'_id': ObjectId(id)})
        return dumps(result[0]), 200

@app.route("/account", methods=['POST', 'GET', 'PATCH'])
def account_list():
    if request.method == 'POST':
        data = request.json

        # Encrypt the password before storing
        encrypted_password = generate_password_hash(data['password'])

        result = mongo.accounts.insert_one({
            'username': data['username'],
            'email': data['email'],
            'role': data['role'],
            'password': encrypted_password,
        })

        return dumps({
            "message": "Account created successfully", 
            "id": str(result.inserted_id) 
        }), 201
    
    elif request.method == 'PATCH':
        data = request.json
        update_data = {
            'username': data['username'],
            'email': data['email'],
            'role': data['role'],
        }

        mongo.accounts.update_one({
            '_id': ObjectId(data['id'])
        }, {
            "$set": update_data
        })

        return jsonify({
            "message": "Account updated successfully",
        }), 200

    elif request.method == 'GET':
        data = mongo.accounts.find()
        accounts = [
            {
                "id": str(account["_id"]),
                "username": account["username"],
                "email": account["email"],
                "role": account["role"],
            } for account in data
        ]
        return dumps(accounts), 200

@app.route("/account/<id>", methods=['PATCH', 'DELETE'])
def account_detail(id):

    if request.method == 'DELETE':
        # Delete a user
        try:
            delete_result = mongo.accounts.delete_one({'_id': ObjectId(id)})
            if delete_result.deleted_count > 0:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/account/password/<id>", methods=['PATCH'])
def account_patch(id):
    # Change password
    try:
        data = request.json
        if 'password' in data:
            from werkzeug.security import generate_password_hash
            new_password = generate_password_hash(data['password'])

            update_result = mongo.accounts.update_one(
                {'_id': ObjectId(id)},
                {"$set": {'password': new_password}}
            )

            if update_result.modified_count > 0:
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                return jsonify({"error": "User not found or no change in password"}), 404
        else:
            return jsonify({"error": "Password is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/room_option", methods=['POST', 'GET','PATCH'])
def room_option():
    if request.method == 'POST':
        data = request.json
        result = mongo.chatHistory.insert_one(data)
        return jsonify({
            "message": "Data inserted successfully",
            "id": str(result.inserted_id) 
        }), 201
    
    elif request.method == 'PATCH':
        data = request.json
        mongo.chatHistory.update_one({
            '_id': ObjectId(data['id'])
        },
        {
            "$set":{
                'chatOption': data['chatOption'],
            }
        })
        return jsonify({
            "message": "Data updated successfully"
        }), 201

    elif request.method == 'GET':
        data = mongo.chatHistory.find()
        return dumps(data), 200

@app.route("/room_option/<id>", methods=['GET', 'DELETE'])
def room_option_by_id(id):
    if request.method == 'DELETE':
        mongo.chatHistory.delete_one({'_id': ObjectId(id)})

        return jsonify({
            "message": "Data Delete successfully",
        }), 201

    elif request.method == 'GET':
        result = mongo.chatHistory.find({'_id': ObjectId(id)})
        return dumps(result[0]), 200

@app.route("/room_line_option", methods=['POST', 'GET','PATCH'])
def room_line_option():
    if request.method == 'PATCH':
        data = request.json
        mongo.lineMessage.update_one({
            '_id': ObjectId(data['id'])
        },
        {
            "$set":{
                'chatOption': data['chatOption'],
            }
        })
        return jsonify({
            "message": "Data updated successfully"
        }), 201

    elif request.method == 'GET':
        data = mongo.lineMessage.find()
        return dumps(data), 200

@app.route("/room_line_option/<id>", methods=['GET', 'DELETE', 'PATCH'])
def room_line_option_by_id(id):
    if request.method == 'DELETE':
        mongo.lineMessage.delete_one({'_id': ObjectId(id)})

        return jsonify({
            "message": "Data Delete successfully",
        }), 201
    
    elif request.method == 'PATCH':
        data = request.json
        mongo.lineMessage.update_one({
            '_id':ObjectId(data['id'])
        },
        {
            '$push': {
                "messages": {
                    '$each': [{
                        'role': 'assistant',
                        'user': 0,
                        'content': data['message'],
                        'timestamp': datetime.now()
                    }]
                }
            }
        })

    elif request.method == 'GET':
        result = mongo.lineMessage.find({'_id': ObjectId(id)})
        return dumps(result[0]), 200

@app.route("/chat_history", methods=['POST', 'GET','PATCH'])
def system_history():
    if request.method == 'POST':
        data = request.json
        result = mongo.chatHistory.find({'_id': ObjectId(data['id'])})
        
        print("result :",result[0])
        mongo.chatHistory.update_one({
            '_id':ObjectId(data['id'])
        },
        {
            '$push': {
                "messages": {
                    '$each': [{
                        'role': 'user',
                        'content': data['message'],
                    }]
                }
            }
        })

        otg = compute_model(
            data['message'],
            result[0]['messages'],
            data['systemPrompt'] if 'systemPrompt' in data else '' ,
            data['temperature'] if 'temperature' in data else 0.5
        )

        message = {
            'role': 'assistant',
            'content': otg,
        }

        mongo.chatHistory.update_one({
            '_id':ObjectId(data['id'])
        },
        {
            '$push': {
                "messages": {
                    '$each': [message]
                }
            }
        })
        
        return message, 200
    
    elif request.method == 'GET':
        data = mongo.chatHistory.find()
        return dumps(data), 200

@app.route("/sending_line_assistant", methods=['POST'])
def sending_line_assistant():
    data = request.json

    setting = mongo.setting.find_one()
    line_bot_api = LineBotApi(setting['line_key'])

    mongo.lineMessage.update_one({
        'line_ids':data['line_ids']
    },
    {
        '$push': {
            "message": {
                '$each': [{
                    'role': 'assistant',
                    'user': 0,
                    'content': data['message'],
                    'timestamp': datetime.now()
                }]
            }
        }
    })

    text_message = TextSendMessage(text=data['message'])
    line_bot_api.push_message(data['line_ids'], text_message)
    return 'OK'
    

@app.route("/message_submit_initial/", methods=['POST','GET'])
def message_submit_initial():

    data = request.json
    id = data['id']
    chatRoom = mongo.chatHistory.count_documents({'_id':ObjectId(id)})

    if chatRoom == 0 :
        mongo.chatHistory.insert_one({
            'chatRoom':{
                'name':data['name'],
                'system_prompt':data['system_prompt'],
                'temperature':data['temperature']
            },
            'message':[
                {
                    'type': 'user',
                    'text': data['message'],
                    'timestamp': datetime.datetime.now()
                },
            ],
        })
    else:
        mongo.chatHistory.update_one({
            '_id':ObjectId(id)
        },
        {
            '$push': {
                "message": {
                    '$each': [{
                        'type': 'user',
                        'text': 'text',
                        'timestamp': datetime.datetime.now()
                    }]
                }
            }
        })
    
    otg = compute_model(
        data['message'],
        chatRoom['message']
    )

    message = {
        'type': 'assistant',
        'room': id,
        'text': otg,
        'timestamp': datetime.datetime.now()
    }

    mongo.chatHistory.update_one({
        '_id':ObjectId(id)
    },
    {
        '$push': {
            "message": {
                '$each': [message]
            }
        }
    })
    
    return message, 200
    
def indexing(text):
    if not text:
        return jsonify({"error": "No text provided"}), 400

    embedding = generate_embedding(text).numpy().flatten().tolist()

    entity = {
        "text": text,
        "embedding": embedding
    }

    logger.info("Indexing new document:")
    logger.debug(f"Text: {text[:100]}...")  # Log first 100 characters of text
    logger.debug(f"Embedding shape: {np.array(embedding).shape}")
    logger.debug(f"Embedding sample: {embedding[:5]}...")  # Log first 5 elements of embedding
    logger.debug(f"Full entity: {entity}")

    insert_result = collection.insert([entity])

    logger.info(f"Insert result: {insert_result}")

    collection.flush()

    return insert_result.primary_keys[0]

@app.route("/callback", methods=['POST','GET'])
def callback():

    req = request.get_json(silent=True, force=True)
    print("Body :", req)
    body = req['messages']
    arr_history = [] if len(body) == 1 else body[0:len(body)-1]
    query = body[0]['content'] if len(body) == 1 else body[len(body)-1]['content']
    data = mongo.systemPrompt.find()

    otg = compute_model(
        query,
        arr_history,
        data[0]['content'],
        data[0]['temperature']
    )

    print("otg : ",otg)

    return [{
        "content": otg,
        "role": 'assistant'
    }], 200

@app.route("/line_callback", methods=['POST','GET'])
def line_callback():

    systemPrompt = mongo.systemPrompt.find_one();
    setting = mongo.setting.find_one();

    print("system_prompt : ",systemPrompt)
    print("setting : ",setting)

    line_bot_api = LineBotApi(setting['line_key'])
    handler = WebhookHandler(setting['line_secret'])

    if 'content' in systemPrompt:
        system_prompt = systemPrompt['content']
    else:
        system_prompt = ''

    if 'temperature' in systemPrompt:
        temperature = systemPrompt['temperature']
    else:
        temperature = 0.4

    if 'greeting' in systemPrompt:
        greeting = systemPrompt['greeting']
    else:
        greeting = None

    req = request.get_json(silent=True, force=True)
    arr_history = []

    for event in req['events']:

        # logger.info(f"pang")
        reply_token = event['replyToken']
        id = event['source']['userId']

        disname = line_bot_api.get_profile(id)
        checkStatus = mongo.lineMessage.find_one({
            'line_ids':id
        })

        logger.info(f"checkStatus {checkStatus}")

        if checkStatus and not checkStatus['chatOption']['botToggle']:
            text = event['message']['text']
            logger.info(f"ping")
            mongo.tempMessage.insert_one({
                'message':{
                    'role': 'user',
                    'user': 0,
                    'content': text,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                'line_ids':disname.user_id
            })

            mongo.lineMessage.update_one({
                'line_ids':id
            },
            {
                '$push': {
                    "message": {
                        '$each': [{
                            'role': 'user',
                            'user': id,
                            'content': text,
                            'timestamp': datetime.now()
                        }]
                    }
                }
            })

        else:

            if checkStatus:
                if 'systemPrompt' in checkStatus['chatOption']:
                    system_prompt = checkStatus['chatOption']['systemPrompt']
                else:
                    system_prompt = ''

                if 'temperature' in checkStatus['chatOption']:
                    temperature = checkStatus['chatOption']['temperature']
                else:
                    temperature = 0.4

                if 'greeting' in checkStatus['chatOption']:
                    greeting = checkStatus['chatOption']['greeting']
                else:
                    greeting = None

            logger.debug(f"event : {event}")
            logger.debug(f"id : {id}")
            logger.debug(f"disname : {disname}")
            text = ''
            datacount = 0

            if event['type'] == 'follow' :

                data = mongo.lineMessage.find({'line_ids':id})
                datacount = mongo.lineMessage.count_documents({'line_ids':id})
                text = greeting if greeting else 'แนะนำตัวพร้อมเสนอบริการให้กับลูกค้าอย่างเหมาะสมและเป็นกันเอง ตามเพศของคุณ และอายุของคุณ แบบสั้นๆ ไม่เกิน 1 บรรทัด'

                logger.debug(f"datacount >>>>>>>>>>>>>>>>> : {datacount}")
            
            elif event['type'] == 'message':
                logger.info(f"pong")
                data = mongo.lineMessage.find({'line_ids':id})
                datacount = mongo.lineMessage.count_documents({'line_ids':id})

                if event['message']['type'] == 'text' :
                    logger.debug(f"disname >>>>>>>>>>>>>> : {disname}")
                    
                    text = event['message']['text']
                    
                    # ws.send(str({"message":text,'user':disname.user_id,'role':'user'}))
                    # response = ws.recv()
                    # sio.emit('new message', {"message":text,'user':disname.user_id,'role':'user'})
                    # sio.wait()

                    mongo.tempMessage.insert_one({
                        'message':{
                            'role': 'user',
                            'user': 0,
                            'content': text,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        },
                        'line_ids':disname.user_id
                    })

                    logger.debug(f"text : {text}")
                    logger.debug(f"datacount : {datacount}")

                    if datacount == 0:
                        mongo.lineMessage.insert_one({
                            'sender':{
                                'displayName':disname.display_name,
                                'language':disname.language,
                                'pictureUrl':disname.picture_url,
                                'userId':disname.user_id,
                            },
                            'chatOption': {
                                'systemPrompt': system_prompt,
                                'temperature': temperature,
                                'botToggle': True,
                            },
                            'message':[
                                {
                                    'role': 'assistant',
                                    'user': 0,
                                    'content': system_prompt,
                                    'timestamp': datetime.now()
                                },
                            ],
                            'line_ids':disname.user_id
                            
                        })
                    else:
                        for ars in data:
                            for mes in ars['message']:
                                arr_history.append({
                                    'role': mes['role'],
                                    'content': mes['content'],
                                })
                        
                        logger.debug(f"Starting ->>>>>>> {arr_history}")
                        
            logger.debug(f"ACCCCCCCCCR ->>>>>>> {arr_history}")
            query = text

            logger.debug(f"system_prompt : {system_prompt}")
            otg = compute_model(
                query,
                arr_history,
                system_prompt if system_prompt else '',
                temperature if temperature else 0.5,
            )

            mongo.lineMessage.update_one({
                'line_ids':id
            },
            {
                '$push': {
                    "message": {
                        '$each': [{
                            'role': 'user',
                            'user': id,
                            'content': text,
                            'timestamp': datetime.now()
                        }]
                    }
                }
            })

            if datacount == 0:
                mongo.lineMessage.insert_one({
                    'sender':{
                        'displayName':disname.display_name,
                        'language':disname.language,
                        'pictureUrl':disname.picture_url,
                        'userId':disname.user_id,
                    },
                    'chatOption': {
                        'systemPrompt': system_prompt,
                        'temperature': temperature,
                        'botToggle': True,
                    },
                    'message':[
                        {
                            'role': 'assistant',
                            'user': 0,
                            'content': otg.replace("\\n", "\n"),
                            'timestamp': datetime.now()
                        },
                    ],
                    'line_ids':disname.user_id
                })
            else:
                mongo.lineMessage.update_one({
                    'line_ids':id
                },
                {
                    '$push': {
                        "message": {
                            '$each': [{
                                'role': 'assistant',
                                'user': id,
                                'content': otg.replace("\\n", "\n"),
                                'timestamp': datetime.now()
                            }]
                        }
                    }
                })

            # ws.send(str({
            #     "message":otg.replace("\\n", "\n"), 
            #     'user':disname.user_id, 
            #     'role':'assistant'
            # }))
            # response = ws.recv()
            # sio.emit('new message', {
            #     "message":otg.replace("\\n", "\n"),
            #     'user':disname.user_id,
            #     'role':'assistant'
            # })
            # sio.wait()
            mongo.tempMessage.insert_one({
                'message':{
                    'role': 'assistant',
                    'user': 0,
                    'content': otg.replace("\\n", "\n"),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                'line_ids':disname.user_id
            })
            text_message = TextSendMessage(text=otg.replace("\\n", "\n"))
            line_bot_api.reply_message(reply_token, text_message)
    
    return 'OK'

@app.route('/short_polling_message', methods=['GET'])
def shortpollingMessage():
    
    tempMessage = mongo.tempMessage.find_one()
    if tempMessage:
        mongo.tempMessage.delete_one({"_id": tempMessage["_id"]})

    return dumps({"message": tempMessage}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # Find user in MongoDB
    user = mongo.accounts.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        # Create JWT access token
        access_token = create_access_token(identity={"id": str(user["_id"]), "username": username})
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Extract the token's unique identifier
    blacklist.add(jti)  # 
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    response = jsonify({"message": "Logout successful"})
    return response, 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    identity = get_jwt_identity()  # Retrieve the username from the token
    user_id = identity.get("id")
    
    # Query the user from MongoDB using the extracted ID or username
    user = mongo.accounts.find_one({'_id': ObjectId(user_id)})

    logger.info(f"user result: {user}")
    if user:
        return jsonify({
            "username": user["username"],
            "email": user.get("email")
        }), 200
    
    return jsonify({"message": "User not found"}), 404

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "Access to protected route granted!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)