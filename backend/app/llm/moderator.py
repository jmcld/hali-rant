from datetime import datetime, timedelta
import uuid
from typing import Dict, Tuple
import sys
import os

# Add the parent directory to the Python path
from ..models.models import (
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
            input=reply.body,
        )
        return moderation.results[0].flagged


# Example usage
if __name__ == "__main__":
    # Initialize moderator
    moderator = ContentModerator()

    # Example rant data using complete mock.json structure
    mock_data = {
        "id": "38ad8e24-3aec-41f9-9742-c23b51d1c781",
        "reply": [
            {
                "id": "746f5262-a28d-4c90-b560-1f5bcdf37169",
                "parent_rant_id": "38ad8e24-3aec-41f9-9742-c23b51d1c781",
                "parent_reply_id": "38ad8e24-3aec-41f9-9742-c23b51d1c781",
                "body": "Harborview Avenue might be nice, but there are many potholes along Beacon Hill Drive and traffic jams near Peninsula Drive.",
                "votes": {"nLike": 19, "nDislike": 16},
                "time": {
                    "created_at": "2025-03-29T16:58:03.060740",
                    "updated_at": "2025-03-29T16:58:03.060740",
                },
                "visible": True,
                "flagged_offensive": False,
            },
            {
                "id": "82fb836d-7892-4dc3-8673-548126994b53",
                "parent_rant_id": "38ad8e24-3aec-41f9-9742-c23b51d1c781",
                "parent_reply_id": "38ad8e24-3aec-41f9-9742-c23b51d1c781",
                "body": "Harborview Ave is scenic, but the potholes near Beacon Hill Dr. ruin the drive. Try Mariners Way instead.",
                "votes": {"nLike": 9, "nDislike": 1},
                "time": {
                    "created_at": "2025-03-29T16:58:03.579698",
                    "updated_at": "2025-03-29T16:58:03.579698",
                },
                "visible": True,
                "flagged_offensive": False,
            },
        ],
        "title": "Smooth Sailing on Harborview Avenue",
        "body": "Harborview Avenue is a smooth and scenic drive from Beacon Hill Drive to Sailors' Cove Park. The well-maintained road offers a peaceful commute with beautiful views of the harbor.",
        "visible": True,
        "flagged_offensive": False,
        "categ": "😊",
        "votes": {"nLike": 29, "nDislike": 17},
        "location": {"lat": 44.62835556991465, "lon": -63.556571638011604},
        "time": {
            "created_at": "2025-03-29T16:58:03.579698",
            "updated_at": "2025-03-29T16:58:03.579698",
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
