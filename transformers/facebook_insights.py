from datetime import datetime

def parse_insights(data):
    out_data = []
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
                            "name": f"{name}_{period}_{k.replace(' ', '_')}",
                            "value": v,
                            "timestamp": end_time
                        }
                    )
            else:
                out_data.append(
                    {
                        "name": f"{name}_{period}",
                        "value": value,
                        "timestamp": end_time
                    }
                )
    return out_data
