from datetime import datetime, timedelta
import uuid
from typing import List, Dict
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data-model"))
from rant_data.models import MessageModel, RantModel, LocationModel, ReplyModel


from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
print(os.getenv('OPENAI_API_KEY'))
# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class ContentModerator:
    def __init__(self):
        # Initialize any moderation-specific settings or models here
        pass

    def load_message(self, message_data: Dict) -> MessageModel:
        """Convert raw message data into a MessageModel instance."""
        # Handle location data
        if "lat" in message_data and "lon" in message_data:
            location = LocationModel(
                lat=message_data["lat"],
                lon=message_data["lon"]
            )
        else:
            raise ValueError("Message must include location data (lat, lon)")

        # Create MessageModel instance
        return MessageModel(
            title=message_data["title"],
            descr=message_data["descr"],
            nLike=message_data.get("nLike", 0),
            nDislike=message_data.get("nDislike", 0),
            loc=location,
            timestamp=message_data.get("timestamp", datetime.utcnow()),
            id=message_data.get("id", uuid.uuid4()),
            parent=message_data.get("parent", 0),
            category=message_data["category"]
        )

    def moderate_message(self, message: MessageModel) -> bool:
        """
        Check if a message is safe and appropriate.
        Returns True if the message is safe, False otherwise.
        """
        # moderate title
        title_moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=message.title,
        )
        response_moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=message.descr,
        )
        
        return response_moderation.results[0].flagged, title_moderation.results[0].flagged


    def moderate_reply(self, reply: ReplyModel) -> bool:
        """
        Check if a rant is safe and appropriate.
        Returns True if the rant is safe, False otherwise.
        """
        # TODO: Implement actual moderation logic here
        # This could include:
        # - Checking for inappropriate content
        # - Validating category
        # - Checking reply content
        return True


# Example usage
if __name__ == "__main__":
    # Initialize moderator
    moderator = ContentModerator()

    # Example message data
    message_data = {
        "title": "Halifax Transit Delays",
        "descr": "The number 1 bus is consistently 15 minutes late during rush hour.",
        "lat": 44.6488,
        "lon": -63.5752,
        "nLike": 45,
        "nDislike": 3,
        "timestamp": datetime.utcnow() - timedelta(hours=2),
        "id": str(uuid.uuid4()),
        "parent": 0,
        "category": "transit"
    }

    # Process message
    message = moderator.load_message(message_data)
    title_is_flagged, descr_is_flagged = moderator.moderate_message(message)
    print(f"title_is_flagged: {title_is_flagged}, descr_is_flagged: {descr_is_flagged}")