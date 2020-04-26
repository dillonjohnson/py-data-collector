#!/usr/bin/env python3
"""Tools for collecting Facebook insights"""

import requests
import datetime
from py_data_collector.sources.common import append_object_id
from functools import partial

FB_VERSION = '6.0'
BASE_URL = f"https://graph.facebook.com/v{FB_VERSION}/"

def _date_to_epoch(_datetime):
    _timestamp = _datetime.timestamp()
    return int(_timestamp)

def _slide_since_and_until(since_dt, until_dt, min_dt):
    until_dt = since_dt
    since_dt = since_dt - datetime.timedelta(days=90)
    if since_dt < min_dt:
        since_dt = min_dt
    return since_dt, until_dt

def is_done(since, query_since):
    """Checks if the pagination should continue or not.

    Args:
        since: the since date sent as the minimum date
        query_since:the since date of the last api call

    Returns:
        A boolean of whether or not the calls are finished.
    """
    return query_since <= since


def _get(object_id, endpoint, params, since, until):
    url = BASE_URL + object_id + "/" + endpoint
    print(f'Calling URL: {url}')
    query_until = until
    diff = until - since
    if diff > datetime.timedelta(days=90):
        query_since = query_until - datetime.timedelta(days=90)
    else:
        query_since = since
    data = []
    is_paging = True
    while is_paging:
        params.update({'since': _date_to_epoch(query_since),
                       'until': _date_to_epoch(query_until)})
        resp = requests.get(url, params).json()
        data.extend(resp.get('data', []))
        if is_done(since, query_since):
            is_paging = False
        else:
            query_since, query_until = _slide_since_and_until(query_since, query_until, since)
    data = list(map(partial(append_object_id, object_id=object_id), data))
    return data


def gather_page_insights(page_id: str,
                         token: str,
                         since: datetime = datetime.datetime.today()-datetime.timedelta(days=1),
                         until: datetime = datetime.datetime.today()):
    """Wraps function to get Facebook insights.

    Args:
        page_id: the social network id of the page
        token: the access token to use in the calls
        since: the datetime to use as the minimum datetime
    """
    params = {
        'access_token': token
    }
    return _get(page_id, 'insights', params=params, since=since, until=until)

# if __name__ == '__main__':
#     data = gather_page_insights('897393153671209',
#                                 'EAAG5Hz1ideoBAEskQ8DUUePxBVQkOOH1vrz4ZAMls4AB96I0e3PZBBLhb6cvEXAyDHgTsMCS25qTBQ4OYAJBS0O2qHuShamkwv7oJWmQZCzGBiKy189QiJV3CeDHdhwVjC4X0owDQWrEUTMHrjU1OlwCg9H0dZAXcXqCf46KFurijTU92ow0cBTMY3MxLZBQZD',
#                                 datetime.datetime(2020, 4, 2),
#                                 datetime.datetime(2020, 4, 3))
#     import pickle
#     pickle.dumps(data)
#     from py_data_collector.transformers.facebook_insights import parse_insights
#     parsed = parse_insights(data)
#     from pprint import pprint
#     # pprint(parsed)
#     finalized = format_for_parquet(parsed)
#     pprint(finalized)
