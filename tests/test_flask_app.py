import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the root endpoint returns 200 and greeting."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from CI Pipeline' in response.data
