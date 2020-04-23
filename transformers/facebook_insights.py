from datetime import datetime
import json

def parse_insights(data):
    out_data = []
    json_payload = json.dumps(data)
    included_in_multi = False
    for d in data:
        name = d['name']
        period = d['period']
        values = d['values']
        for obj in values:
            end_time = datetime.strptime(obj['end_time'], '%Y-%m-%dT%H:%M:%S+0000') if obj.get('end_time') else datetime.utcnow()
            value = obj['value']
            if isinstance(value, dict):
                for k, v in value.items():
                    out_data.append(
                        {
                            "name": f"{name}_{period}",
                            "subname": k.replace(' ', '_'),
                            "value": v,
                            "effective_timestamp": end_time,
                            "json_payload": "" if included_in_multi else json_payload
                        }
                    )
                    included_in_multi = True
            else:
                out_data.append(
                    {
                        "name": f"{name}_{period}",
                        "value": value,
                        "effective_timestamp": end_time,
                        "json_payload": json_payload
                    }
                )
    return out_data
