# import facebook
import requests
import logging
import datetime

FB_VERSION = '6.0'
BASE_URL = f"https://graph.facebook.com/v{FB_VERSION}/"

def _date_to_epoch(dt):
    ts = dt.timestamp()
    return int(ts)

def _slide_since_and_until(since_dt, until_dt, min_dt):
    until_dt = since_dt
    since_dt = since_dt - datetime.timedelta(days=90)
    if since_dt < min_dt:
        since_dt = min_dt
    return since_dt, until_dt

def is_done(since, query_since):
    if query_since <= since:
        return True
    else:
        return False


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

def gather_page_insights(page_id,
                         token,
                         since=datetime.datetime.today()-datetime.timedelta(days=1),
                         until=datetime.datetime.today()):
    params = {
        'metric': 'post_activity,page_impressions_organic,page_fan_removes,page_places_checkin_mobile,page_impressions,page_places_checkin_total,page_posts_impressions_organic_unique,page_consumptions_unique,page_impressions_organic_unique,page_engaged_users,page_posts_impressions,page_fan_removes_unique,page_posts_impressions_viral_unique,page_posts_impressions_paid_unique,page_impressions_unique,page_negative_feedback,page_content_activity_unique,page_negative_feedback_unique,page_fan_adds_unique,page_consumptions,page_fan_adds,page_impressions_paid_unique,page_places_checkin_total_unique,page_posts_impressions_viral,page_content_activity,post_activity_unique,post_negative_feedback_unique,page_posts_impressions_paid,page_places_checkin_mobile_unique,page_impressions_paid,page_impressions_viral_unique,page_impressions_viral,page_fans,post_negative_feedback,page_posts_impressions_unique',
        'access_token': token
    }
    return _get(page_id, 'insights', params=params, since=since, until=until)

if __name__ == '__main__':
    gather_page_insights('897393153671209',
                         'EAAG5Hz1ideoBAEskQ8DUUePxBVQkOOH1vrz4ZAMls4AB96I0e3PZBBLhb6cvEXAyDHgTsMCS25qTBQ4OYAJBS0O2qHuShamkwv7oJWmQZCzGBiKy189QiJV3CeDHdhwVjC4X0owDQWrEUTMHrjU1OlwCg9H0dZAXcXqCf46KFurijTU92ow0cBTMY3MxLZBQZD',
                         datetime.datetime(2020, 3,1),
                         datetime.datetime(2020,4,1))