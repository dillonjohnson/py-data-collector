#!/usr/bin/env python3
"""Tools for collecting Facebook post backfill"""

import requests
import datetime
from py_data_collector.sources.common import append_object_id
from py_data_collector.transformers.facebook_post_backfill import parse_facebook_backfill
from functools import partial

FB_VERSION = '6.0'
BASE_URL = f"https://graph.facebook.com/v{FB_VERSION}/"

def _get(page_id: str,
         params: dict):
    url = f'{BASE_URL}/{page_id}/posts'
    data = []
    is_paging = True
    while is_paging:
        resp = requests.get(
            next_url if 'next_url' in vars() else url,
            params=params
        ).json()
        data.extend(resp.get('data', []))
        next = resp.get('paging', {}).get('next', None)
        if next:
            next_url = next
        else:
            is_paging = False
    data = list(map(partial(
        append_object_id,
        object_id=page_id
    ), data))
    return data

def gather_page_backfill(page_id: str,
                         token: str,
                         fields: str):
    """Wraps function to get Facebook post backfill.

    Args:
        page_id: the social network id of the page
        token: the access token to use in the calls
    """
    params = {
        'access_token': token,
        'fields': fields
    }
    return _get(page_id, params)

if __name__ == '__main__':
    d = gather_page_backfill('897393153671209',
                             'EAACjUX8PXfMBADIv1Laq4KlZCVckBuvMl5sTrbLK3rCO3vJtYRZAZBjSp0WBcpNGZCIX6uyE8ZBesYZCyPdZCnBySrhx1MSK0ZAE7mU9nJZAyGDUXKyDsSMonvQ1TCpHTdSzrtKptWZC7cx88PhzvUlXGnG8GstGNnP7oVwL3UFPJZA880ZCTblGKwdweeGlrHbCZCUtaA4b4PqhfzjODSTFNZACES',
                             'attachments{title,description},picture,is_published,created_time,comments.summary(1).limit(1),shares,likes.summary(1).limit(1)')
    parsed = parse_facebook_backfill(d)
    print(parsed)
