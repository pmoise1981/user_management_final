import httpx

BASE_URL = "http://localhost:8000"

register_payload = {
    "email": "admin@example.com",
    "password": "adminpassword",
    "role": "ADMIN"
}

response = httpx.post(f"{BASE_URL}/register/", json=register_payload)

if response.status_code == 200:
    print("✅ User registered successfully.")
    print(response.json())
else:
    print(f"❌ Failed to register: {response.status_code}")
    print(response.text)

