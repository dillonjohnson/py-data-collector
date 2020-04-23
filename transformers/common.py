def format_for_parquet(data):
    new_arr = []
    for d in data:
        new_arr.append(
            {
                "processed_timestamp": "",
                "effective_timestamp": "",
                "month": "",
                "year": "",
                "json_payload": "",
                "social_network_id": ""
            }
        )