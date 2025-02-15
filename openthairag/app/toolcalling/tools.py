tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get Current Time from Localtion name",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": 'The location name (City, Province, State, or Country) to get the datetime in english only',
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_more_product_detail",
            "description": "Get more detail or picture from user quation such as ขอข้อมูลเพิ่มเติม or ขอตัวอย่าง or ขอรูปภาพ",
            "parameters": { 
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "the type of service is only product or service",
                    },
                },
                "required": ["category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "insert_feedback",
            "description": "Get feedback from users to improve and develop. staff or product",
            "parameters": { 
                "type": "object",
                "name": {
                    "type": "string",
                    "description": 'the title of feedback about explaination of feedback that is good or bad feedback',
                },
                "detail": {
                    "type": "string",
                    "description": 'detail of feedback about product or service',
                },
                "user_name": {
                    "type": "string",
                    "description": 'name of user when feedback to system',
                },
                "required": [
                    "name",
                    "detail",
                    "user_name"
                ],
            },
        },
    },
]

def get_tools():
    return tools