#-*- coding: UTF-8 -*-
from geopy.geocoders import Nominatim 
from timezonefinder import TimezoneFinder 
from datetime import datetime
import pytz
import os
from bson import ObjectId
from db import Connection

API_URL = os.environ.get('API_URL', 'hhttp://localhost:5500')
mongo=Connection('otg_db')

def get_current_time(location):
    geolocator = Nominatim(user_agent="otg_app") 
    
    location = geolocator.geocode(location) 
    obj = TimezoneFinder() 
    
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude) 
    print("Time Zone : ", result) 
    return {
        "time_now": get_datetime_now(result)
    }

def get_product_recommand(category):

    setting = mongo.setting.find_one()
    if not setting['product_activate']:
        return {'message': 'Product is not activated'}

    products = mongo.products.find({'category': category})
    print(f"Products count : {products}")
    return {
        "products": [{
            "name": f"{item["name"]}",
            "detail": f"{item["detail"]}",
            "category": f"{item["category"]}",
            "pictures": list(map(lambda picture: f"{API_URL}/{picture}", item["picture"])),        
        } for item in products]
    }
    

def insert_feedback(name, detail, user_name):

    setting = mongo.setting.find_one()
    if not setting['feedback_activate']:
        return {'message': 'Feedback is not activated'}

    mongo.issues.insert_one({
        "name": name,
        "detail": detail,
        "user_name":  user_name,
        "created_at": datetime.utcnow()
    })
    
    return {
        "message": "Feedback inserted successfully",
    }

def get_datetime_now(timezone: str):
    tz = pytz.timezone(timezone)
    return datetime.now(tz).isoformat()
