import httpx
from fastapi.testclient import TestClient

class TestAuth:
    # ------------------------- SIGNUP TESTS -------------------------
    def test_signup_success(self, client: TestClient):
        payload = {
            "email": "test@example.com",
            "password": "securepassword"
        }
        response = client.post("/signup", json=payload)
        assert response.status_code == 200, f"Response: {response.text}"
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
        assert "password" not in data

    def test_signup_duplicate_email(self, client: TestClient):
        payload = {
            "email": "duplicate@example.com",
            "password": "password123"
        }
        response1 = client.post("/signup", json=payload)
        assert response1.status_code == 200

        response2 = client.post("/signup", json=payload)
        assert response2.status_code == 400, f"Response: {response2.text}"
        assert "Email already registered" in response2.text

    def test_signup_invalid_email(self, client: TestClient):
        payload = {
            "email": "invalid-email",
            "password": "password123"
        }
        response = client.post("/signup", json=payload)
        assert response.status_code == 422, f"Response: {response.text}"
        assert "email" in response.text

    def test_signup_missing_email(self, client: TestClient):
        payload = {"password": "password123"}
        response = client.post("/signup", json=payload)
        assert response.status_code == 422, f"Response: {response.text}"

    def test_signup_missing_password(self, client: TestClient):
        payload = {"email": "test@example.com"}
        response = client.post("/signup", json=payload)
        assert response.status_code == 422, f"Response: {response.text}"

    # ------------------------- LOGIN TESTS -------------------------
    def test_login_success(self, client: TestClient):
        # Create user first
        signup_payload = {
            "email": "login@example.com",
            "password": "correctpassword"
        }
        client.post("/signup", json=signup_payload)

        # Test login
        login_payload = {
            "email": "login@example.com",
            "password": "correctpassword"
        }
        response = client.post("/login", json=login_payload)
        assert response.status_code == 200, f"Response: {response.text}"
        token = response.json()
        assert "access_token" in token
        assert isinstance(token["access_token"], str)

    def test_login_invalid_email(self, client: TestClient):
        login_payload = {
            "email": "nonexistent@example.com",
            "password": "whatever"
        }
        response = client.post("/login", json=login_payload)
        assert response.status_code == 401, f"Response: {response.text}"
        assert "Invalid credentials" in response.text

    def test_login_invalid_password(self, client: TestClient):
        # Create user
        signup_payload = {
            "email": "user@example.com",
            "password": "rightpassword"
        }
        client.post("/signup", json=signup_payload)

        # Test wrong password
        login_payload = {
            "email": "user@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/login", json=login_payload)
        assert response.status_code == 401, f"Response: {response.text}"
        assert "Invalid credentials" in response.text

    def test_login_missing_email(self, client: TestClient):
        payload = {"password": "password"}
        response = client.post("/login", json=payload)
        assert response.status_code == 422, f"Response: {response.text}"

    def test_login_missing_password(self, client: TestClient):
        payload = {"email": "test@example.com"}
        response = client.post("/login", json=payload)
        assert response.status_code == 422, f"Response: {response.text}"