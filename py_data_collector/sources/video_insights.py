# import facebook
import requests
import datetime

FB_VERSION = '6.0'
BASE_URL = f"https://graph.facebook.com/v{FB_VERSION}/"

def _get(object_id, endpoint, params):
    url = BASE_URL + object_id + "/" + endpoint
    print(f'Calling URL: {url}')
    data = requests.get(url, params=params).json()['data']
    return data

def gather_video_insights(page_id,
                         token,
                         since=datetime.datetime.today()-datetime.timedelta(days=1),
                         until=datetime.datetime.today()):
    params = {
        'access_token': token
    }
    return _get(page_id, 'video_insights', params=params)

if __name__ == '__main__':
    data = gather_video_insights('2611719889065046',
                                'EAAG5Hz1ideoBAEskQ8DUUePxBVQkOOH1vrz4ZAMls4AB96I0e3PZBBLhb6cvEXAyDHgTsMCS25qTBQ4OYAJBS0O2qHuShamkwv7oJWmQZCzGBiKy189QiJV3CeDHdhwVjC4X0owDQWrEUTMHrjU1OlwCg9H0dZAXcXqCf46KFurijTU92ow0cBTMY3MxLZBQZD')
    from py_data_collector.transformers.facebook_insights import parse_insights
    parsed = parse_insights(data)
    from pprint import pprint
    pprint(parsed)