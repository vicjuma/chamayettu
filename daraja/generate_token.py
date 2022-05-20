import requests
from django.conf import settings

def generate_token():
    url = settings.ACCESS_TOKEN_URL

    queryString = {"grant_type": "client_credentials"}

    headers = {
        "Content-Type": "application/json"
    }

    username = settings.CONSUMER_KEY
    password = settings.CONSUMER_SECRET

    res = requests.get(url, headers=headers, auth=(
        username, password), params=queryString)
        
    if res.status_code == 200:
        return res.json()['access_token']
    return None