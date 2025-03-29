from datetime import datetime, timedelta
import uuid
from typing import Dict, Tuple
import sys
import os

# Add the parent directory to the Python path
from backend.app.models.models import (
    RantModel,
    LocationModel,
    ReplyModel,
    VotableModel,
    TimeModel,
)

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ContentModerator:
    def __init__(self, model: str = "omni-moderation-latest"):
        # Initialize any moderation-specific settings or models here
        self.model = model

    @staticmethod
    def load_rant(rant_data: Dict) -> RantModel:
        """Convert raw rant data into a RantModel instance."""

        # Handle location data
        location = LocationModel(**rant_data["location"])

        # Handle votes data
        votes = VotableModel(**rant_data["votes"])

        # Handle time data
        time = TimeModel(**rant_data["time"])

        # Create RantModel instance
        kwargs = {
            k: v for k, v in rant_data.items() if k not in {"location", "votes", "time"}
        }
        return RantModel(location=location, votes=votes, time=time, **kwargs)

    @staticmethod
    def load_reply(reply_data: Dict) -> RantModel:
        kwargs = {k: v for k, v in reply_data.items() if k not in {"votes", "time"}}
        return ReplyModel(
            votes=VotableModel(**reply_data["votes"]),
            time=TimeModel(**reply_data["time"]),
            **kwargs,
        )

    def moderate_rant(self, rant: RantModel) -> RantModel:
        """
        Check if a rant is safe and appropriate.
        Returns a Tuple of (body_is_flagged, title_is_flagged).
        """
        # moderate title
        title_moderation = client.moderations.create(
            model=self.model,
            input=rant.title,
        )
        # moderate body
        body_moderation = client.moderations.create(
            model=self.model,
            input=rant.body,
        )

        # update rant, if either offensive title or body, flag!
        is_flagged = (
            body_moderation.results[0].flagged or title_moderation.results[0].flagged
        )
        rant.flagged_offensive = is_flagged
        if is_flagged:
            rant.visible = False
        return rant

    def moderate_reply(self, reply: ReplyModel) -> bool:
        """
        Check if a reply is safe and appropriate.
        Returns True if the reply is safe, False otherwise.
        """
        # moderate msg
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
        "id": "c2be3b8e-3147-4ca4-af15-b2c4125e708d",
        "reply": [
            {
                "id": "8f4d0ac7-94a3-4f06-bb66-d954c979e8a5",
                "rantId": "c2be3b8e-3147-4ca4-af15-b2c4125e708d",
                "msg": "I agree! The roads are terrible. Let's hope they fix them soon. #FrustratedDrivers",
                "votes": {"nLike": 0, "nDislike": 0},
                "time": {
                    "created_at": "2025-03-29T16:02:00.315937",
                    "updated_at": "2025-03-29T16:02:00.315937",
                },
                "visible": True,
                "flagged_offensive": False,
            },
            {
                "id": "dadab7d2-f4e1-4e0f-9c50-7c8104a7f417",
                "rantId": "c2be3b8e-3147-4ca4-af15-b2c4125e708d",
                "msg": "I agree! Potholes are such a nuisance. Let's hold officials accountable for better roads.",
                "votes": {"nLike": 0, "nDislike": 0},
                "time": {
                    "created_at": "2025-03-29T16:02:00.853818",
                    "updated_at": "2025-03-29T16:02:00.853818",
                },
                "visible": True,
                "flagged_offensive": False,
            },
        ],
        "title": '"Potholes Everywhere: Fix the Roads Now!"',
        "body": "Sick of dodging potholes every day! Fix the roads already - tired of wasting money on constant car repairs! #InfrastructureFail.",
        "visible": True,
        "flagged_offensive": False,
        "categ": "\ud83d\ude2d",
        "votes": {"nLike": 0, "nDislike": 0},
        "location": {"lat": 44.66283067128525, "lon": -63.56144854342206},
        "time": {
            "created_at": "2025-03-29T16:02:00.853818",
            "updated_at": "2025-03-29T16:02:00.853818",
        },
    }
    # Process rant
    rant = moderator.load_rant(mock_data)
    rant_is_flagged = moderator.moderate_rant(rant)
    print(f"rant_is_flagged: {rant_is_flagged}")

    # Process each reply from the mock data
    for reply_data in mock_data["reply"]:
        reply = moderator.load_reply(reply_data)
        reply_is_flagged = moderator.moderate_reply(reply)
        print(f"Reply is_flagged: {reply_is_flagged}")
