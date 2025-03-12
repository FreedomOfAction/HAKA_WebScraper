import json

def clean_data(data):
    """Removes unnecessary characters and formats extracted information."""
    data["broker_name"] = data["broker_name"].strip().title()
    data["supported_assets"] = [asset.strip() for asset in data["supported_assets"]]
    return data

def to_json(data):
    """Converts extracted data to a JSON format."""
    return json.dumps(data, indent=4)
