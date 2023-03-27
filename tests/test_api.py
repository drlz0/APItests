import json
import requests
import pytest
from random import randint
from randominfo import get_first_name

ENDPOINT = "https://simple-books-api.glitch.me"


# check api status

def test_check_status():
    response = requests.get(ENDPOINT + '/status')
    assert response.status_code == 200


# check list of books and validate response


def test_list_of_books():
    payload = {
        "type": "fiction",
    }
    response = requests.get(ENDPOINT + "/books", params=payload)
    data = response.json()
    assert response.status_code == 200

    only_fiction = [x for x in data if x["type"] == "fiction"]
    assert only_fiction[0]["type"] == "fiction"


# def test_register():
#     payload = client_data()
#     headers = {
#         'Content-Type': 'application/json'
#     }

#     response = requests.post(
#         ENDPOINT+"/api-clients/", headers=headers, data=payload)
#     assert response.status_code == 201


def test_get_single_book():
    book_id = 4
    response = requests.get(ENDPOINT + f"/books/{book_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == book_id


def test_order_book(auth_token):
    token = auth_token["accessToken"]
    payload = json.dumps({
        "bookId": 4,
        "customerName": "Arnold"
    })

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(ENDPOINT + "/orders", headers=headers, data=payload)
    assert response.status_code == 201


def test_get_all_book_orders(auth_token):
    token = auth_token["accessToken"]
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(ENDPOINT + '/orders', headers=headers)
    assert response.status_code == 200


def test_get_an_order(auth_token):
    token = auth_token["accessToken"]
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(ENDPOINT + '/orders', headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    data = response_data[0]["id"]
    response = requests.get(ENDPOINT + f'/orders/{data}', headers=headers)
    assert response.status_code == 200


def test_update_order(auth_token):
    token = auth_token["accessToken"]
    name = "John"
    payload = json.dumps({
        "customerName": name
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(ENDPOINT + '/orders', headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    data = response_data[0]["id"]

    response = requests.patch(ENDPOINT + f'/orders/{data}', headers=headers, data=payload)
    assert response.status_code == 204

    response = requests.get(ENDPOINT + f'/orders/{data}', headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["customerName"] == name


def test_delete_oder(auth_token):
    token = auth_token["accessToken"]
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(ENDPOINT + '/orders', headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    data = response_data[0]["id"]

    response = requests.delete(ENDPOINT + f'/orders/{data}', headers=headers)
    assert response.status_code == 204

    response = requests.get(ENDPOINT + f'/orders/{data}', headers=headers)
    assert response.status_code == 404


def client_data():
    email = get_first_name() + f"{randint(1, 1000)}" + "@" + "example.com"
    return json.dumps({
        "clientName": "Arnold",
        "clientEmail": f"{email}"
    })


@pytest.fixture(scope="session")
def auth_token():
    payload = client_data()
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", ENDPOINT + "/api-clients/", headers=headers, data=payload)
    response_data = response.json()
    return response_data
