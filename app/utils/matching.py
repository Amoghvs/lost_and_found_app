import base64
from urllib.parse import urlparse
from rapidfuzz.fuzz import partial_ratio
from app.utils.minio import minio_client
from openai import OpenAI
import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ["API_KEY"])

def get_image_base64_from_url(image_url: str, bucket_name: str = "lostfound") -> str:
    try:
        # Parse and extract only the object name
        parsed_url = urlparse(image_url)
        object_name = parsed_url.path.lstrip("/")  # removes leading '/'

        response = minio_client.get_object(bucket_name, object_name)
        image_data = response.read()
        return base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        print(f"Error retrieving image {image_url}: {e}")
        return None


def llm_match_score(lost_item, found_item) -> int:
    lost_image_b64 = get_image_base64_from_url(lost_item.image_url)
    found_image_b64 = get_image_base64_from_url(found_item.image_url)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
You are a helpful assistant that scores the similarity between a LOST item and a FOUND item.

You are given two images and metadata.

Respond with a number from 0 (completely unrelated) to 100 (perfect match).

LOST ITEM:
Title: {lost_item.title}
Description: {lost_item.description}
Location: {lost_item.location_lat}, {lost_item.location_lng}

FOUND ITEM:
Title: {found_item.title}
Description: {found_item.description}
Location: {found_item.location_lat}, {found_item.location_lng}

Evaluate if these two items match based on text AND image similarity.
Only respond with the number.
"""
                }
            ]
        }
    ]

    # Add lostimage 1
    if lost_image_b64:
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{lost_image_b64}"
            }
        })

    # Add found image (originally found image)
    if found_image_b64:
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{found_image_b64}"
            }
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        score = int(response.choices[0].message.content.strip())
        return min(max(score, 0), 100)
    except Exception as e:
        print("LLM error:", e)
        return 0

def compute_match_score(new_item, existing_item):
    title_score = partial_ratio(new_item.title, existing_item.title)
    desc_score = partial_ratio(new_item.description, existing_item.description)

    # Combine local score using weights
    local_score = 0.5 * title_score + 0.5 * desc_score

    # Get LLM-based match score
    llm_score = llm_match_score(new_item, existing_item)

    # Final score is the average of both
    final_score = (local_score + llm_score) / 2
    print(f"Title Score: {title_score}, Description Score: {desc_score}, LLM Score: {llm_score}, Final Score: {final_score}")
    return round(final_score, 2)
