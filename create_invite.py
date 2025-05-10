import asyncio
import httpx

# Use the nginx service name, which reverse proxies to FastAPI
BASE_URL = "http://nginx"

LOGIN_DATA = {
    "username": "admin@example.com",
    "password": "adminpassword"
}

INVITE_DATA = {
    "email": "invitee@example.com"
}

async def main():
    async with httpx.AsyncClient() as client:
        # Login to get token
        response = await client.post(f"{BASE_URL}/login/", data=LOGIN_DATA)
        if response.status_code != 200:
            print("❌ Login failed:", response.status_code, response.text)
            return

        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        # Create invite
        invite_response = await client.post(f"{BASE_URL}/invites/", json=INVITE_DATA, headers=headers)
        if invite_response.status_code == 200:
            print("✅ Invite created:", invite_response.json())
        else:
            print("❌ Failed to create invite:", invite_response.status_code, invite_response.text)

if __name__ == "__main__":
    asyncio.run(main())

