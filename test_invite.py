import httpx

BASE_URL = "http://localhost:8000"

# Replace these with your actual test credentials
LOGIN_DATA = {
    "username": "admin@example.com",
    "password": "yourpassword"
}

def get_token():
    response = httpx.post(f"{BASE_URL}/login/", data=LOGIN_DATA)
    response.raise_for_status()
    return response.json()["access_token"]

def create_invite(email, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(f"{BASE_URL}/invites/", json={"email": email}, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        token = get_token()
        print("✅ Token retrieved.")

        result = create_invite("test@example.com", token)
        print("✅ Invite created:")
        print(result)
    except httpx.HTTPStatusError as err:
        print(f"❌ Error: {err.response.status_code}")
        print(err.response.text)

