from flask import request, jsonify
from db import Connection
from bson.json_util import dumps
from bson import ObjectId
import datetime
import logging
import requests
from processing import compute_model

from linebot.models import *
from linebot import *
import re

mongo=Connection('otg_db')
logger = logging.getLogger(__name__)

def room_fb_option_get():
    data = list(mongo.fbMessage.find())
    return jsonify({
            "data": [ {**doc, "_id": str(doc["_id"])} for doc in data ]
        }), 200

def room_fb_option_patch(data):
    mongo.fbMessage.update_one({
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

# =============================

def room_fb_option_by_id_get(id):
    result = mongo.fbMessage.find({'_id': ObjectId(id)})
    return dumps(result[0]), 200

def room_fb_option_by_id_patch(data, id):
    mongo.fbMessage.update_one({
            '_id':ObjectId(id)
        },
        {
            '$push': {
                "messages": {
                    '$each': [{
                        'role': 'assistant',
                        'user': 0,
                        'content': data['message'],
                        'timestamp': datetime.datetime.now()
                    }]
                }
            }
        })
    
def room_fb_option_by_id_delete(id):
    mongo.fbMessage.delete_one({'_id': ObjectId(id)})

    return jsonify({
        "message": "Data Delete successfully",
    }), 201

# =============================

def room_line_option_patch(data):
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

def room_line_option_get():
    data = mongo.lineMessage.find()
    return jsonify({
        "data": [ {**doc, "_id": str(doc["_id"])} for doc in data ]
    }), 200

# =============================

def room_line_option_by_id_get(id):
    mongo.lineMessage.find_one({'_id': ObjectId(id)})

    return jsonify({
        "message": "Data Delete successfully",
    }), 201
    
def room_line_option_by_id_patch(data):
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
                    'timestamp': datetime.datetime.now()
                }]
            }
        }
    })

def room_line_option_by_id_delete(id):
    result = mongo.lineMessage.delete_many({'_id': ObjectId(id)})
    return dumps(result[0]), 200

# =============================

def room_option_post(data):
    result = mongo.chatHistory.insert_one(data)
    return jsonify({
        "message": "Data inserted successfully",
        "id": str(result.inserted_id) 
    }), 201
    
def room_option_patch(data):
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

def room_option_get(args):
    username = args.get('account_owner')
    data = mongo.chatHistory.find({
        'account_owner': username
    })
    return dumps(data), 200

# =============================

def room_option_by_id_delete(id):

    mongo.chatHistory.delete_one({'_id': ObjectId(id)})
    
    return jsonify({
        "message": "Data Delete successfully",
    }), 201

def room_option_by_id_get(id):
    result = mongo.chatHistory.find({'_id': ObjectId(id)})
    return dumps(result[0]), 200

# =============================

def system_history_post(data):
    result = mongo.chatHistory.find_one({'_id': ObjectId(data['id'])})
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
        result['messages'],
        data['systemPrompt'] if 'systemPrompt' in data else '' ,
        data['temperature'] if 'temperature' in data else 0.5
    )

    message = {
        'role': 'assistant',
        'content': otg['content'],
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

    if (len(result['messages']) < 3):
        res = compute_model(
            'ช่วยตั้งชื่อบทสนทนาให้หน่อย ขอแค่ชื่อเท่านั้น',
            result['messages'],
            data['systemPrompt'] if 'systemPrompt' in data else '' ,
            data['temperature'] if 'temperature' in data else 0.5
        )

        mongo.chatHistory.update_one({
            '_id':ObjectId(data['id'])
        },
        {
            '$set': {
                'chatOption': {
                    "name": res['content'].replace('"', ''),
                    "temperature": result['chatOption']['temperature'],
                    "systemPrompt": result['chatOption']['systemPrompt']
                }
            }
        })
    
    return {
        "title_name": res['content'].replace('"', '') if result['chatOption']['name'] == "" else result['chatOption']['name'],
        "message": message
    }, 200

def system_history_get(data):
    data = mongo.chatHistory.find()
    return dumps(data), 200

# =============================

def callback(data):

    req = data
    print("Body :", req)
    body = req['messages']
    arr_history = [] if len(body) == 1 else body[0:len(body)-1]
    query = body[0]['content'] if len(body) == 1 else body[len(body)-1]['content']
    data = mongo.systemPrompt.find_one()

    otg = compute_model(
        query,
        arr_history,
        data['systemPrompt'] if 'systemPrompt' in data else '' ,
        data['temperature'] if 'temperature' in data else 0.5
    )

    return [{
        "content": otg['content'].replace('"', ''),
        "role": 'assistant'
    }], 200

def line_callback(data):
    systemPrompt = mongo.systemPrompt.find_one()
    setting = mongo.setting.find_one()

    print("system_prompt : ",systemPrompt)
    print("setting : ",setting)

    if setting['line_activate'] == False:
        return 'OK'

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

    req = data
    arr_history = []

    for event in req['events']:

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
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                            'timestamp': datetime.datetime.now()
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

                    mongo.tempMessage.insert_one({
                        'message':{
                            'role': 'user',
                            'user': 0,
                            'content': text,
                            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                                    'timestamp': datetime.datetime.now()
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

            logger.debug(f"otg : {otg}")
            
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
                            'timestamp': datetime.datetime.now()
                        }]
                    }
                }
            })

            mongo.lineMessage.update_one({
                'line_ids':id
            },
            {
                '$push': {
                    "message": {
                        '$each': [{
                            'role': 'assistant',
                            'user': id,
                            'content': otg['content'].replace("\\n", "\n"),
                            'timestamp': datetime.datetime.now()
                        }]
                    }
                }
            })

            mongo.tempMessage.insert_one({
                'message':{
                    'role': 'assistant',
                    'user': 0,
                    'content': otg['content'].replace("\\n", "\n"),
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                'line_ids':disname.user_id
            })

            parts = process_text(otg['content'])
            print(f"parts =>>>>>>> : {parts}")
            for part in parts:
                if is_valid_image_url(part):

                    print(f"Image =>>>>>>> : {part}")
                    text_message = ImageSendMessage(
                        original_content_url=part, 
                        preview_image_url=part
                    )
                    line_bot_api.push_message(id, text_message)
                elif part not in ['-', ',', ''] and len(part) > 1:
                    text_message = TextSendMessage(text=part)
                    line_bot_api.push_message(id, text_message)
    
    return 'OK'

def fb_callback_get(args):
    setting = mongo.setting.find_one()
    if args.get("hub.mode") == "subscribe" and args.get("hub.challenge"):
        if not args.get("hub.verify_token") == setting['facebook_verify_password']:
            return "Verification token missmatch", 403
        return args['hub.challenge'], 200
    return "Hello world", 200
    
def fb_callback_post(data):
    systemPrompt = mongo.systemPrompt.find_one()
    setting = mongo.setting.find_one()

    if setting['line_activate'] == False:
        return 'OK'

    arr_history = []
    # print(f"data respona : {data}")

    if 'message' not in data['entry'][0]['messaging'][0]:
        return 'OK'
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    query = message

    data = mongo.fbMessage.find({'fb_ids':sender_id})
    for ars in data:
        for mes in ars['message']:
            print(f'mes : {mes['mid']} {query['mid']} {mes['mid'] == query['mid']}')
            if mes['mid'] == query['mid']:
                return 'OK'

            arr_history.append({
                'role': mes['role'],
                'content': mes['content'],
            })

    mongo.fbTempMessage.find_one({})

    # print("system_prompt : ",systemPrompt)
    # print("setting : ",setting)
    # print("sender_id : ",sender_id)

    API = "https://graph.facebook.com/v13.0/me/messages?access_token="+setting['facebook_token']
    API_PROFILE = "https://graph.facebook.com/"+sender_id+"?fields=first_name,last_name,profile_pic&access_token="+setting['facebook_token']

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

    checkStatus = mongo.fbMessage.find_one({
        'fb_ids':sender_id
    })

    # logger.info(f"checkStatus {checkStatus}")

    if checkStatus and not checkStatus['chatOption']['botToggle']:
        text = message
        
        mongo.fbTempMessage.insert_one({
            'message':{
                'role': 'user',
                'user': sender_id,
                'content': query['text'],
                'mid': query['mid'],
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'fb_ids':sender_id
        })

        mongo.fbMessage.update_one({
            'fb_ids':sender_id
        },
        {
            '$push': {
                "message": {
                    '$each': [{
                        'role': 'user',
                        'user': sender_id,
                        'content': query['text'],
                        'mid': query['mid'],
                        'timestamp': datetime.datetime.now()
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

        
        

        datacount = mongo.fbMessage.count_documents({'fb_ids':sender_id})

        res =  requests.get(API_PROFILE).json()

        mongo.fbTempMessage.insert_one({
            'message':{
                'role': 'user',
                'user': sender_id,
                'content': query['text'],
                'mid': query['mid'],
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'fb_ids':sender_id
        })

        if datacount == 0:
            mongo.fbMessage.insert_one({
                'sender':{
                    'displayName':res['first_name']+' '+res['last_name'],
                    'pictureUrl':res['profile_pic'],
                    'userId':sender_id,
                },
                'chatOption': {
                    'systemPrompt': system_prompt,
                    'temperature': temperature,
                    'botToggle': True,
                },
                'message':[
                    {
                        'role': 'user',
                        'mid': query['mid'],
                        'user': sender_id,
                        'content': query['text'],
                        'timestamp': datetime.datetime.now()
                    },
                ],
                'fb_ids':sender_id
                
            })
        else:
            # print(f"mama gonegone : {query}")
            mongo.fbMessage.update_one({
                'fb_ids':sender_id
            },
            {
                '$push': {
                    "message": {
                        '$each': [{
                            'role': 'user',
                            'mid': query['mid'],
                            'user': sender_id,
                            'content': query['text'],
                            'timestamp': datetime.datetime.now()
                        }]
                    }
                }
            })

        otg = compute_model(
            query['text'],
            arr_history,
            system_prompt if system_prompt else '',
            temperature if temperature else 0.4,
        )

        mongo.fbMessage.update_one({
            'fb_ids':sender_id
        },
        {
            '$push': {
                "message": {
                    '$each': [{
                        'role': 'assistant',
                        'user': sender_id,
                        'mid': None,
                        'content': otg['content'].replace("\\n", "\n"),
                        'timestamp': datetime.datetime.now()
                    }]
                }
            }
        })
            
        mongo.fbTempMessage.insert_one({
            'message':{
                'role': 'assistant',
                'user': 0,
                'content': otg['content'].replace("\\n", "\n"),
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'fb_ids':sender_id
        })


        parts = process_text(otg['content'])
        print(f"parts =>>>>>>> : {parts}")
        for part in parts:
            if is_valid_image_url(part):
                request_body = {
                    "recipient": {
                        "id": sender_id
                    },
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {
                                "url": part,
                                "is_reusable": True
                            }
                        }
                    }
                }
                print(f"Imaging =>>>>>>>> {part}")
                response = requests.post(API, json=request_body).json()

            elif part not in ['-', ',', ''] and len(part) > 1:
                request_body = {
                    "recipient": {
                        "id": sender_id
                    },
                    "message": {
                        "text": part
                    }
                }
                response = requests.post(API, json=request_body).json()

    return 'OK'

# =============================

def sending_line_assistant(data):

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
                    'timestamp': datetime.datetime.now()
                }]
            }
        }
    })

    text_message = TextSendMessage(text=data['message'])
    line_bot_api.push_message(data['line_ids'], text_message)
    return 'OK'

# =============================

def sending_fb_assistant(data):
    setting = mongo.setting.find_one()

    API = "https://graph.facebook.com/v13.0/me/messages?access_token="+setting['facebook_token']

    print(f'config : {setting} {data}')
    mongo.fbMessage.update_one({
        'fb_ids':data['sending_id']
    },
    {
        '$push': {
            "message": {
                '$each': [{
                    'role': 'assistant',
                    'user': 0,
                    'content': data['message'],
                    'timestamp': datetime.datetime.now()
                }]
            }
        }
    })

    request_body = {
        "recipient": {
            "id": data['sending_id']
        },
        "message": {
            "text": data['message']
        }
    }
    response = requests.post(API, json=request_body).json()
    return 'OK'

# =============================

def message_submit_initial(data):

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
                    'timestamp': datetime.datetime.datetime.now()
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
                        'timestamp': datetime.datetime.datetime.now()
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
        'text': otg['content'],
        'timestamp': datetime.datetime.datetime.now()
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

# =============================

def fbshortpollingMessage():
    
    tempMessage = mongo.fbTempMessage.find_one()
    if tempMessage:
        mongo.fbTempMessage.delete_one({"_id": tempMessage["_id"]})

    return dumps({"message": tempMessage}), 200

def shortpollingMessage():
    
    tempMessage = mongo.tempMessage.find_one()
    if tempMessage:
        mongo.tempMessage.delete_one({"_id": tempMessage["_id"]})

    return dumps({"message": tempMessage}), 200

# =============================

def resetLineMessage(data):
    mongo.tempMessage.delete_many({"line_ids": data["send_id"]})
    return 'OK', 200

def resetFBMessage(data):
    mongo.fbTempMessage.delete_many({"fb_ids": data["fb_ids"]})
    return 'OK', 200

# =============================


def process_text(input: str):
    regex = r"!?\[.*?\]\((.*?)\)"
    # regex = r"!?\[.*?\]\((https?://[^\s)]+)\)"
    parts = []

    last_index = 0
    for match in re.finditer(regex, input):
        # Add the part of the text before the current match
        if last_index != match.start():
            parts.append(input[last_index:match.start()].strip())
        # Add the matched image markdown
        if match.group(0).startswith('!'):
            parts.append(match.group(1))
        else:
            parts.append(match.group(0).strip())

        last_index = match.end()

    # Add the remaining text after the last match
    if last_index < len(input):
        parts.append(input[last_index:].strip())

    return parts

def is_valid_image_url(url: str) -> bool:
    regex = r"^http.*\.(jpg|png)$"
    return bool(re.match(regex, url))

