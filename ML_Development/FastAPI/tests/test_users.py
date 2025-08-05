from urllib import response
from app import schemas
from jose import jwt
from app.config import settings
    
# def test_root(client, session):
#     response = client.get("/")
#     print(response.json().get('message'))
#     assert response.json().get('message') == 'Hello World'
#     assert response.status_code == 200
    
def test_create_user(client):
    response = client.post("/users", json={"email": "osborn@gmail.com", "password": "password1234"})
    
    random_user = schemas.UserCreateResponse(**response.json())
    assert random_user.email == 'osborn@gmail.com'
    
    # Store the JSON in a variable first
    new_user = response.json()
    print(new_user) # Now you can print it
    
    # Assertions
    assert new_user.get('email') == 'osborn@gmail.com'
    assert 'created_at' in new_user # Check if the key exists
    assert response.status_code == 201
    
def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    
    
    assert response.status_code == 200