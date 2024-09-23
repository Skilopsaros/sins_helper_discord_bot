import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

def set_bot_avatar(image_path):
    """
    Sets an animated avatar for a Discord bot using the token from the .env file.

    Parameters:
    - image_path: str. The path to the animated GIF to set as the avatar.
    """
    
    access_token = os.getenv('TOKEN')

    
    url = 'https://discord.com/api/v9/users/@me'
    
    
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    avatar_data = f'data:image/gif;base64,{base64_image}'

    headers = {
        'Authorization': f'Bot {access_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'avatar': avatar_data,
    }

    response = requests.patch(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Avatar updated successfully.")
    else:
        print(f"Failed to update avatar. Status code: {response.status_code}, Response: {response.text}")

image_path = 'animated_avatar.gif'
set_bot_avatar(image_path)