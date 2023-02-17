import requests
import datetime
import time

from django.conf import settings

from diversity.celery import app
from main_app import models


@app.task
def update_info() -> None:
    print('TASKA STARTANULA')
    token = settings.OPENAPI_TOKEN
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    url = f'https://serverru.eyezon.online/public/api/buttons'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    button_id = requests.get(
        url,
        headers=headers,
    ).json()
    button_id = button_id[0]['_id']
    workers_list_url = f'https://serverru.eyezon.online/public/api/buttons/{button_id}/workers/'
    streamers = requests.get(workers_list_url, headers=headers).json()
    for streamer_index in range(0, len(streamers)):
        streamer = streamers[streamer_index]['_id']
        stats_url = f'https://serverru.eyezon.online/api/button/{button_id}/worker/{streamer}/stat?from={date}&to={date}&limit=100&offset=0'
        stats = requests.get(
            stats_url,
            headers=headers,
        ).json()
        dialogs = [dialog for dialog in stats['dialogs']]
        for dialog in dialogs:
            if not models.DataModel.objects.filter(createdAt=dialog['createdAt']).exists():
                duration = int(dialog['duration'])
                duration = time.strftime('%H:%M:%S', time.gmtime(duration / 1000.0))
                models.DataModel.objects.create(
                    title=dialog['title'],
                    createdAt=dialog['createdAt'],
                    logUrl=dialog['logUrl'],
                    websiteUrl=dialog['websiteUrl'],
                    rating=dialog['rating'],
                    streamsNumber=dialog['streamsNumber'],
                    isStreamMade=dialog['isStreamMade'],
                    duration=duration,
                )
    print('TASKA GG')