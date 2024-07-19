import requests


def test_add_scooter(base_url):
    response = requests.post(f"{base_url}/scooters", json={
        "location": "Downtown",
        "status": "available"
    })
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    data = response.json()
    assert "scooter_id" in data, "Response JSON does not contain 'scooter_id'"
    assert data["location"] == "Downtown", f"Expected location 'Downtown' but got {data['location']}"
    assert data["status"] == "available", f"Expected status 'available' but got {data['status']}"


def test_add_scooter_with_invalid_status(base_url):
    response = requests.post(f"{base_url}/scooters", json={
        "location": "Downtown",
        "status": "broken"
    })
    assert response.status_code == 400, f"Expected status code 400 for invalid status but got {response.status_code}"
