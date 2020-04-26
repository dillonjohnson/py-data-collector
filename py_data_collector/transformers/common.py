from datetime import datetime

def format_for_parquet(data):
    new_arr = []
    for d in data:
        effective_timestamp = d['effective_timestamp']
        d['processed_timestamp'] = datetime.utcnow()
        d['month'] = '{0:0=2d}'.format(effective_timestamp.month)
        d['year'] = '{0:0=4d}'.format(effective_timestamp.year)
        new_arr.append(
            d
        )
    return new_arr