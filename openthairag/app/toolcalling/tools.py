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
            "name": "get_product_recommand",
            "description": "Get the product for present to user When a user asks something that he wants to know the answer to, such as what to eat tonight, you can search for food information with this function to present to the user by entering the following categories: food, service, travel",
            "parameters": { 
                "type": "object",
                "category": {
                    "type": "string",
                    "description": 'the category name of product (only food, service, travel )',
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