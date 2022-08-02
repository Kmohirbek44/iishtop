import asyncio
import os, sys

import asyncio as asyncio
from django.contrib.auth import get_user_model
from django.db import DatabaseError



proj = os.path.dirname(os.path.abspath('manage.py'))

sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'API_project.settings'
import django

django.setup()
import scraping.models
from scraping.parsers import *

parser = (
    (hh, 'hh'),
    (ishkop, 'ishkop'),
    (uzjobble, 'uzjobble'),

)
jobs = []

User = get_user_model()


def get_user():
    city = scraping.models.City.objects.all().values()
    language = scraping.models.Language.objects.all().values()
    settings_lst = set((c['id'], l['id']) for c in city for l in language)
    return settings_lst


def get_urls(_settings):
    qs = scraping.models.Urls.objects.all().values()
    dict_url = {(q['city_id'], q['language_id']): q['data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['data'] = dict_url[pair]
        urls.append(tmp)
    return urls


async def main(value):

    func , url, city, language = value
    job = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)


a = get_user()
get_url = get_urls(a)
loop = asyncio.new_event_loop()
tmp_tasks = [(func, data['data'][key], data['city'], data['language'])
             for data in get_url for func, key in parser]


tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()
for job in jobs:

    if isinstance(job,dict):
        v = scraping.models.Vakation(**job)
        v.save()

