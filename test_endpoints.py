import config
import pytest
from sqlalchemy import create_engine,text
import json
database=create_engine(config.test_config['DB_URL'],encoding='utf-8',max_overflow=0)
#테스트 설정을 읽어들여 test 데이터베이스에 접속한다. 

from app import create_app

@pytest.fixture
def api():
    app=create_app(config.test_config)
    app.config['TEST']=True
    api=app.test_client()

    return api

def test_ping(api):
    resp=api.get('/ping')
    assert b'pong' in resp.data

def test_tweet(api):
    new_user={
            'email' :'songwe2@gmail.com',
            'password':'test password2',
            'name':'song2',
            'profile':'test profile2'
            }
    resp=api.post(
            '/sign-up',
            data=json.dumps(new_user),
            content_type='application/json'
            )
    assert resp.status_code == 200

    resp_json=json.loads(resp.data.decode('UTF-8'))
    new_user_id=resp_json['id']

    resp=api.post(
            '/login',
            data=json.dumps({'email':'songwe2@gmail.com','password':'test password2'}),
            content_type='application/json'
            )
    resp_json=json.loads(resp.data.decode('utf-8'))
    access_token=resp_json['access_token']

    resp=api.post(
            '/tweet',
            data=json.dumps({'tweet':"Hello World!"}),
            content_type='application/json',
            headers={'Authorization':access_token}
            )
    assert resp.status_code == 200

    resp=api.get(f'/timeline/{new_user_id}')
    tweets=json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id' :2,
        'timeline':[
            {
                'user_id':2,
                'tweet':"Hello World!"
                }
            ]
        }

