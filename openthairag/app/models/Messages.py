from datetime import datetime
from bson.objectid import ObjectId

class Messages:
    def __init__(self, sender, message, datetime=None, _id=None):
        self.sender = sender
        self.message = message
        self.datetime = datetime if datetime else datetime.utcnow()
        self._id = _id if _id else ObjectId()

    def to_dict(self):
        return {
            "sender": self.sender,
            "message": self.message,
            "datetime": self.datetime,
            "_id": self._id,
        }
    
    @staticmethod
    def from_dict(data):
        return Messages(
            sender=data.get('sender'),
            message=data.get('message'),
            datetime=data.get('datetime'),
            _id=data.get('_id')
        )
    
    def __repr__(self):
        return f"Message ('{self.sender}', '{self.message}')"