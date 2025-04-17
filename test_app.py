import pytest
import json
from app import app, db, calculate_points

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    with app.app_context():
        db.drop_all()

def test_process_receipt_valid(client):
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ],
        "total": "35.35"
    }
    response = client.post('/receipts/process', json=receipt_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data

    receipt_id = data['id']
    points_response = client.get(f'/receipts/{receipt_id}/points')
    assert points_response.status_code == 200
    points_data = json.loads(points_response.data)
    assert points_data['points'] == 28

def test_process_receipt_invalid_data(client):
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "invalid-date",
        "purchaseTime": "13:01",
        "items": [],
        "total": "35.35"
    }
    response = client.post('/receipts/process', json=receipt_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['description'] == "The receipt is invalid."

def test_get_points_not_found(client):
    response = client.get('/receipts/nonexistent-id/points')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['description'] == "Invalid receipt ID format."

def test_calculate_points_example_1():
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ],
        "total": "35.35"
    }
    points = calculate_points(receipt_data)
    assert points == 28

def test_calculate_points_example_2():
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    }
    points = calculate_points(receipt_data)
    assert points == 109
