
import requests
import django
import time
from asgiref.sync import sync_to_async
import os
import sys
from django import setup
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv
child_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(child_directory)
sys.path.append(os.path.join(parent_directory, 'Cake_Bot'))
print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cake_Bot.settings')

from property.models import ClickCounter
def update_clicks():
    link = urlparse('https://vk.cc/cJrYMm')
    counter = ClickCounter.objects.first()
    load_dotenv()
    token = os.getenv("VK_SERVICE_ACCESS_KEY")
    print(token)
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link.path.replace('/', ''),
        'interval': 'forever'
    }
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats',
                            params=params)
    response.raise_for_status()
    api_response = response.json()
    if 'error' in api_response:
        return
    print(api_response['response'])
    if 'stats' in api_response['response'] and len(api_response['response']['stats']) > 0:
        views = int(api_response['response']['stats'][0]['views'])
        print(int(api_response['response']['stats'][0]['views']))
    else:
        print('Ошибка')
        views = 0
    counter.clicks = views
    counter.save()
    
