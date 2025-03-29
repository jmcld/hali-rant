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
    def __init__(self, model: str = "omni-moderation-latest"):
        # Initialize any moderation-specific settings or models here
        self.model = model

    @staticmethod
    def load_rant(rant_data: Dict) -> RantModel:
        """Convert raw rant data into a RantModel instance."""
        
        # Handle location data
        location = LocationModel(
            **rant_data["location"]
        )
       
        # Handle votes data
        votes = VotableModel(
            **rant_data["votes"]
        )

        # Handle time data
        time = TimeModel(
            **rant_data["time"]
        )

        # Create RantModel instance
        kwargs = {k: v for k, v in rant_data.items() if k not in {"location", "votes", "time"}}
        return RantModel(
            location=location,
            votes=votes,
            time=time,
            **kwargs
        )

    @staticmethod
    def load_reply(reply_data: Dict) -> RantModel:
        kwargs = {k: v for k, v in reply_data.items() if k not in {"votes", "time"}}
        return ReplyModel(
            votes=VotableModel(**reply_data["votes"]),
            time=TimeModel(
                **reply_data["time"]
            ),
            **kwargs
        )
        
    def moderate_rant(self, rant_data) -> Tuple[bool, bool]:
        """
        Check if a rant is safe and appropriate.
        Returns a Tuple of (body_is_flagged, title_is_flagged).
        """
        # load rant
        rant = self.load_rant(rant_data)
        # moderate title
        title_moderation = client.moderations.create(
            model=self.model,
            input=rant.title,
        )
        body_moderation = client.moderations.create(
            model=self.model,
            input=rant.body,
        )

        return body_moderation.results[0].flagged or title_moderation.results[0].flagged

    def moderate_reply(self, reply_data: Dict) -> bool:
        """
        Check if a reply is safe and appropriate.
        Returns True if the reply is safe, False otherwise.
        """
        # load reply 
        reply = self.load_reply(reply_data)
        moderation = client.moderations.create(
            model=self.model,
            input=reply.msg,
        )
        return moderation.results[0].flagged


# Example usage
if __name__ == "__main__":
    # Initialize moderator
    moderator = ContentModerator()

    # Example rant data using complete mock.json structure
    mock_data = {
        "id": "e95616cf-fb01-46a5-8cf9-3643b58d9d1f",
        "reply": [
            {
                "id": "2a88427c-f0e1-4b66-99fa-267745574f96",
                "rantId": "5cf75dfb-b18d-46eb-8083-05166df75451",
                "msg": "It is a bad pot hole!",
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
                "msg": "You should watch the road when you drive",
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

    # Process rant
    rant_is_flagged = moderator.moderate_rant(mock_data)
    print(f"rant_is_flagged: {rant_is_flagged}")

    # Process each reply from the mock data
    for reply_data in mock_data["reply"]:
        reply_is_flagged = moderator.moderate_reply(reply_data)
        print(f"Reply is_flagged: {reply_is_flagged}")