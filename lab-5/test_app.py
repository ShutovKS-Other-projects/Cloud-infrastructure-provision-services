import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"API" in response.data

def test_user_crud(client):
    response_post = client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
    assert response_post.status_code == 201
    assert b"uspeshno sozdan" in response_post.data

    response_get = client.get('/users')
    assert response_get.status_code == 200
    assert b"testuser" in response_get.data
    
    users = response_get.get_json()
    assert len(users) == 1
    user_id = users[0]['id']

    response_put = client.put(f'/users/{user_id}', json={'username': 'testuser_updated'})
    assert response_put.status_code == 200
    assert b"uspeshno obnovleny" in response_put.data

    response_delete = client.delete(f'/users/{user_id}')
    assert response_delete.status_code == 200
    assert b"uspeshno udalen" in response_delete.data

    response_get_final = client.get('/users')
    assert response_get_final.status_code == 200
    assert b"testuser" not in response_get_final.data


def test_caching(client):
    response1 = client.get('/report')
    assert response1.status_code == 200
    data1 = response1.get_json()

    response2 = client.get('/report')
    assert response2.status_code == 200
    data2 = response2.get_json()

    assert data1['generated_at'] == data2['generated_at']