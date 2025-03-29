import json
from openai import OpenAI
from datetime import datetime
import uuid
import os
from typing import Tuple
import random

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define topic categories and their associated emojis
TOPICS = {
    "infrastructure": {
        "emoji": "🚧",
        "examples": ["roads", "sidewalks", "construction", "potholes", "traffic lights", "bike lanes"],
    }
    # },
    # "transit": {
    #     "emoji": "🚌",
    #     "examples": ["buses", "ferry", "bus stops", "schedules"]
    # }
}

def get_random_topic():
    """
    Get a random topic and its associated emoji
    """
    topic_name = random.choice(list(TOPICS.keys()))
    topic_data = TOPICS[topic_name]
    example = random.choice(topic_data["examples"])
    return topic_name, topic_data["emoji"], example


def generate_rant_content(is_positive: bool = None) -> Tuple[str, str, str]:
    """
    Generate a random rant title and body using OpenAI with separate calls
    """
    try:
        # Randomly decide if this will be a positive or negative post if not specified
        if is_positive is None:
            is_positive = random.choice([True, False])

        # Get random topic and example
        topic_name, _, topic_example = get_random_topic()
        
        # Set emoji based on sentiment
        emoji = "😊" if is_positive else "😠"
        
        sentiment = "positive feedback" if is_positive else "complaint"
        tone = "satisfied" if is_positive else "frustrated"

        # Generate title
        title_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a {tone} citizen in Halifax, using an app to write about specific locations. Use specific, made-up street names and intersections that sound realistic for Halifax (e.g., 'Bluenose Drive', 'Harbor View Road', 'Atlantic Street', 'Maritime Avenue'). Respond with only a brief title (under 50 characters) for a {sentiment} about {topic_name}. Do not use hashtags.",
                },
                {"role": "user", "content": f"Generate a title for a {sentiment} about {topic_example}."},
            ],
        )
        title = title_response.choices[0].message.content.strip().strip('"\'\\/').replace('\\', '')

        # Generate body based on the title
        body_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a {tone} citizen in Halifax. Write about a specific location using made-up but realistic-sounding Halifax street names (e.g., 'Lighthouse Lane', 'Ocean Breeze Court', 'Scotia Square Drive', 'Dockyard Road'). Write a brief {sentiment} (under 200 characters) about this {topic_name} topic. Reference specific intersections or landmarks.  Do not use hashtags.",
                },
                {"role": "user", "content": f"Write a short {sentiment} about: {title}"},
            ],
        )
        body = body_response.choices[0].message.content.strip().strip('"\'\\/').replace('\\', '')

        return title, body, emoji
    except Exception as e:
        print(f"Error generating content: {e}")
        return "City Topic", "There's something happening in the city.", "🏙️"


def generate_reply(title: str, body: str) -> str:
    """
    Generate a reply to a rant using OpenAI
    """
    try:
        # Randomly choose if the reply agrees or disagrees with the original post
        agrees = random.choice([True, False])
        stance = "agreeing with" if agrees else "disagreeing with"
        
        reply_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a citizen {stance} someone's post about Halifax. Reference specific locations using made-up but realistic street names (e.g., 'Mariner's Way', 'Salt Spray Road', 'Anchor Street', 'Peninsula Drive'). Keep your response under 100 characters and make it sound natural.  Do not use hashtags.",
                },
                {
                    "role": "user",
                    "content": f"Write a brief reply {stance} this post - Title: {title}, Content: {body}.  Do not use hashtags.",
                },
            ],
        )
        reply = reply_response.choices[0].message.content.strip().strip('"\'\\/').replace('\\', '')
        return reply
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "I have thoughts about this too!"


def create_mock_rant(is_positive: bool = None):
    """
    Create a complete mock rant entry with generated content
    """
    title, body, emoji = generate_rant_content(is_positive)

    min_lat = 44.57
    max_lat = 44.73
    min_lon = -63.70  # Note: West longitudes are negative
    max_lon = -63.52
    
    # Generate random coordinates within the box
    random_lat = random.uniform(min_lat, max_lat)
    random_lon = random.uniform(min_lon, max_lon)

    # Generate random number of initial votes (1-5)
    initial_votes = random.randint(1, 5)
    
    # Initialize vote counters
    total_likes = initial_votes if is_positive else 0
    total_dislikes = 0 if is_positive else initial_votes

    rant_id = str(uuid.uuid4())
    
    # Generate 0-5 replies
    num_replies = random.randint(0, 5)
    replies = []
    for _ in range(num_replies):
        reply_msg = generate_reply(title, body)
        reply_time = datetime.now().isoformat()
        
        # Random likes and dislikes for reply
        reply_likes = random.randint(0, 20)
        reply_dislikes = random.randint(0, 20)
        
        # Add reply votes to totals
        total_likes += reply_likes
        total_dislikes += reply_dislikes
        
        replies.append({
            "id": str(uuid.uuid4()),
            "rantId": rant_id,
            "msg": reply_msg,
            "votes": {
                "nLike": reply_likes,
                "nDislike": reply_dislikes
            },
            "time": {
                "created_at": reply_time,
                "updated_at": reply_time,
            },
            "visible": True,
            "flagged_offensive": False
        })

    return {
        "id": rant_id,
        "reply": replies,
        "title": title,
        "body": body,
        "visible": True,
        "flagged_offensive": False,
        "categ": emoji,
        "votes": {
            "nLike": total_likes,
            "nDislike": total_dislikes
        },
        "location": {"lat": random_lat, "lon": random_lon},
        "time": {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
    }

import tqdm
def generate_mock_data(num_rants: int = 100):
    """
    Generate multiple mock rants and save to JSON file
    """
    # Ensure a mix of positive and negative posts
    rants = []
    for i in tqdm.tqdm(range(num_rants)):
        # Force alternating positive/negative if more than one rant
        is_positive = not bool(i % 5) if num_rants > 1 else None
        rants.append(create_mock_rant(is_positive))

    with open("data-model/mock_rants.json", "w", encoding='utf-8') as f:
        json.dump(rants, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    generate_mock_data()
