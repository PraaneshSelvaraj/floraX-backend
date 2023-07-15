import requests
import json
import base64
from includes import keys

def detect_plant(image):
    url = 'https://api.plant.id/v2/identify'
    encoded_string = base64.b64encode(image.read())

    base64_string = encoded_string.decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Api-Key": keys.plant_id
    }

    data = {
        "images": [base64_string],
        "organs": ["flower", "leaf"],
        "organs_number": 5
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    resp = json.loads(response.text)
    
    if "suggestions" in resp and len(resp["suggestions"]) > 0:
        return resp["suggestions"][0]
    else:
        return None

def detect_diesease(image):
    url = 'https://api.plant.id/v2/health_assessment'
    encoded_string = base64.b64encode(image.read())

    base64_string = encoded_string.decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Api-Key": keys.plant_id
    }

    data = {
        "images": [base64_string],
        "organs": ["flower", "leaf"],
        "organs_number": 5
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    resp = json.loads(response.text)
    try:
        if "health_assessment" in resp:
            data = {}
            data['healthy'] = resp['health_assessment']['is_healthy']
            data['health_probality'] = resp['health_assessment']['is_healthy_probability']
            data['disease'] = resp['health_assessment']['diseases'][0]['name']
            return data
        else: return None

    except Exception as e: 
        print(e)
        return None
