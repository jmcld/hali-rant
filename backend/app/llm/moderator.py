from datetime import datetime, timedelta
import uuid
from typing import Dict, Tuple
import sys
import os

# Add the parent directory to the Python path
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data-model"))
from backend.app.models.models import RantModel, LocationModel, ReplyModel, VotableModel, TimeModel

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class ContentModerator:
    def __init__(self):
        # Initialize any moderation-specific settings or models here
        pass

    def load_rant(self, rant_data: Dict) -> RantModel:
        """Convert raw rant data into a RantModel instance."""
        # Handle location data
        if "lat" in rant_data and "lon" in rant_data:
            location = LocationModel(
                lat=rant_data["lat"],
                lon=rant_data["lon"]
            )
        else:
            raise ValueError("Rant must include location data (lat, lon)")

        # Handle votes data
        votes = VotableModel(
            nLike=rant_data.get("nLike", 0),
            nDislike=rant_data.get("nDislike", 0)
        )

        # Handle time data
        now = datetime.utcnow()
        time = TimeModel(
            created_at=rant_data.get("timestamp", now),
            updated_at=now
        )

        # Create RantModel instance
        return RantModel(
            id=rant_data.get("id", uuid.uuid4()),
            title=rant_data["title"],
            body=rant_data["body"],
            categ=rant_data["category"],
            location=location,
            votes=votes,
            time=time,
            reply=[]  # Initialize with empty replies
        )

    def moderate_rant(self, rant: RantModel) -> Tuple[bool, bool]:
        """
        Check if a rant is safe and appropriate.
        Returns a Tuple of (body_is_flagged, title_is_flagged).
        """
        # moderate title
        title_moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=rant.title,
        )
        body_moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=rant.body,
        )
        
        return body_moderation.results[0].flagged, title_moderation.results[0].flagged

    def moderate_reply(self, reply: ReplyModel) -> bool:
        """
        Check if a reply is safe and appropriate.
        Returns True if the reply is safe, False otherwise.
        """
        moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=reply.msg,
        )
        return not moderation.results[0].flagged


# Example usage
if __name__ == "__main__":
    import json
    from datetime import datetime

    # Initialize moderator
    moderator = ContentModerator()

    # Example rant data using complete mock.json structure
    mock_data = {
        "id": "e95616cf-fb01-46a5-8cf9-3643b58d9d1f",
        "reply": [
            {
                "id": "2a88427c-f0e1-4b66-99fa-267745574f96",
                "rantId": "5cf75dfb-b18d-46eb-8083-05166df75451",
                "msg": "I know mine too!",
                "votes": {
                    "nLike": 0,
                    "nDislike": 0
                },
                "time": {
                    "created_at": "2025-03-29T12:06:04.844408",
                    "updated_at": "2025-03-29T12:06:04.844415"
                }
            },
            {
                "id": "310acf65-d646-49a2-9cdf-b47e8ed0c75b",
                "rantId": "7f0d0cfa-0922-4cb6-bb83-5c517d3fb849",
                "msg": "You should watch the road when you drive.",
                "votes": {
                    "nLike": 0,
                    "nDislike": 0
                },
                "time": {
                    "created_at": "2025-03-29T12:06:04.844408",
                    "updated_at": "2025-03-29T12:06:04.844415"
                }
            }
        ],
        "title": "Potholes",
        "body": "This pothole destroyed my car",
        "categ": "😭",
        "votes": {
            "nLike": 0,
            "nDislike": 0
        },
        "location": {
            "lat": 44.0,
            "lon": -63.0
        },
        "time": {
            "created_at": "2025-03-29T12:06:04.844408",
            "updated_at": "2025-03-29T12:06:04.844415"
        }
    }

    # Convert the mock data into our input format
    rant_data = {
        "title": mock_data["title"],
        "body": mock_data["body"],
        "lat": mock_data["location"]["lat"],
        "lon": mock_data["location"]["lon"],
        "nLike": mock_data["votes"]["nLike"],
        "nDislike": mock_data["votes"]["nDislike"],
        "timestamp": datetime.fromisoformat(mock_data["time"]["created_at"]),
        "id": mock_data["id"],
        "category": mock_data["categ"]
    }

    # Process rant
    rant = moderator.load_rant(rant_data)
    body_is_flagged, title_is_flagged = moderator.moderate_rant(rant)
    print(f"body_is_flagged: {body_is_flagged}, title_is_flagged: {title_is_flagged}")

    # Process each reply from the mock data
    for reply_data in mock_data["reply"]:
        reply = ReplyModel(
            id=uuid.UUID(reply_data["id"]),
            rantId=uuid.UUID(reply_data["rantId"]),
            msg=reply_data["msg"],
            votes=VotableModel(**reply_data["votes"]),
            time=TimeModel(
                created_at=datetime.fromisoformat(reply_data["time"]["created_at"]),
                updated_at=datetime.fromisoformat(reply_data["time"]["updated_at"])
            )
        )
        reply_is_flagged = moderator.moderate_reply(reply)
        print(f"Reply '{reply.msg}' is_flagged: {not reply_is_flagged}")