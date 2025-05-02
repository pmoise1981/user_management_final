import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_invite_route(async_client: AsyncClient, admin_token):
    response = await async_client.post(
        "/invites/",
        json={"email": "invitee@example.com"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "token" in data
    assert data["email"] == "invitee@example.com"


@pytest.mark.asyncio
async def test_get_invite_by_token_route(async_client: AsyncClient, admin_token):
    # First create the invite
    create_resp = await async_client.post(
        "/invites/",
        json={"email": "lookup@example.com"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 200
    invite = create_resp.json()

    # Then fetch it by ID
    fetch_resp = await async_client.get(
        f"/invites/{invite['id']}"
    )

    assert fetch_resp.status_code == 200
    fetched = fetch_resp.json()
    assert fetched["email"] == "lookup@example.com"
    assert fetched["id"] == invite["id"]

