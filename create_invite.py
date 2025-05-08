import httpx

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJBRE1JTiIsImV4cCI6MTc0NjczMjc1Mn0.jLgblEZPOiIoccvGh3gdmWPoicdJY9JDZdBsIIaKp8I"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

data = {
    "email": "invitee@example.com"
}

response = httpx.post("http://localhost:8000/invites/", headers=headers, json=data)

if response.status_code == 200:
    print("✅ Invite created successfully.")
    print(response.json())
else:
    print("❌ Failed to create invite:", response.status_code)
    print(response.text)

