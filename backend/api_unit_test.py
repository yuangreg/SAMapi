import json
from backend import app

def test_ping():
    response = app.test_client().get('/ping')
    res = json.loads(response.data.decode('utf-8')).get("message")
    assert res == 'pong'

def test_predict_everything():
    IMAGE_PATH = './images/cat.jpg'
    params = {'mode': 'everything'}
    payload = json.dumps(params)
    data = {
        "data": payload,
        'image': (open(IMAGE_PATH, 'rb'), IMAGE_PATH),
    }
    response = app.test_client().post('/predict', data=data)
    assert response.status_code == 200


def test_predict_bbox():
    IMAGE_PATH = './images/cat.jpg'
    params = {
        'mode': 'box',
        'box_prompt': [0.1, 0.1, 0.4, 0.5],
    }
    payload = json.dumps(params)
    data = {
        "data": payload,
        'image': (open(IMAGE_PATH, 'rb'), IMAGE_PATH),
    }
    response = app.test_client().post('/predict', data=data)
    assert response.status_code == 200


def test_predict_text():
    IMAGE_PATH = './images/cat.jpg'
    params = {
        'mode': 'text',
        'text_prompt': 'a photo of a dog',
    }
    payload = json.dumps(params)
    data = {
        "data": payload,
        'image': (open(IMAGE_PATH, 'rb'), IMAGE_PATH),
    }
    response = app.test_client().post('/predict', data=data)
    assert response.status_code == 200


def test_predict_points():
    IMAGE_PATH = './images/cat.jpg'
    params = {
        'mode': 'points',
        'point_prompt': [[0.8, 0.4]],
        'point_label': [1],
    }
    payload = json.dumps(params)
    data = {
        "data": payload,
        'image': (open(IMAGE_PATH, 'rb'), IMAGE_PATH),
    }
    response = app.test_client().post('/predict', data=data)
    assert response.status_code == 200


test_ping()
test_predict_everything()
test_predict_bbox()
test_predict_text()
test_predict_points()