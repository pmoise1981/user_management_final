# login_user.py
import httpx

login_url = "http://localhost:8000/login/"
payload = {
    "username": "admin@example.com",
    "password": "adminpassword"
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = httpx.post(login_url, data=payload, headers=headers)

if response.status_code == 200:
    token = response.json().get("access_token")
    print("✅ Login successful.")
    print("🔐 Access Token:", token)
else:
    print("❌ Login failed:", response.status_code)
    print(response.text)

