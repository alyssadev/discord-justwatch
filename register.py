import requests
from os import environ

url = f"https://discord.com/api/v8/applications/{environ['JWBOT_CLIENT_ID']}/guilds/{environ['JWBOT_TARGET_GUILD']}/commands"

json = {
    "name": "watch",
    "description": "Look up a movie or show on JustWatch to see what service you would need for it",
    "options": [
        {
            "name": "name",
            "description": "The name of the movie or show you want to watch",
            "type": 3,
            "required": True
        },
        {
            "name": "_type",
            "description": "The type of thing you want to watch (movie, show)",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "Movie",
                    "value": "movie"
                },
                {
                    "name": "Show",
                    "value": "show"
                }
            ]
        },
        {
            "name": "result_count",
            "description": "How many movie/show results you want to see (default is 3)",
            "type": 4,
            "required": False
        },
        {
            "name": "dontskipnonfree",
            "description": "Do you want to include results that aren't free or fixed rate (e.g Apple)",
            "type": 5,
            "required": False
        }
    ]
}

with open(".bottoken") as f:
    headers = {"Authorization": "Bot " + f.read().strip()}

print(requests.post(url, headers=headers, json=json).json())
