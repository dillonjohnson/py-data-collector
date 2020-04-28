from datetime import datetime
from dateutil import parser
import json

def parse_facebook_backfill(data):
    out_data = []
    for item in data:
        json_value = json.dumps(item)
        processed_timestamp = datetime.utcnow()
        social_network_id = item['object_id']
        timestamp = parser.parse(item['created_time'])
        out_data.append(
            {
                'json-payload': json_value,
                'effective_timestamp': timestamp,
                'processed_timestamp': processed_timestamp,
                'social_network_id': social_network_id,
                'month': '%02d' % timestamp.month,
                'year': '%04d' % timestamp.year
            }
        )
    return out_data