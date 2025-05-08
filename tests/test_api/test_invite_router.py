import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_invite_unauthorized(async_client: AsyncClient):
    response = await async_client.post("/invites/", json={"email": "fail@example.com"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_invite_invalid_email(async_client: AsyncClient, admin_token):
    response = await async_client.post(
        "/invites/",
        json={"email": "not-an-email"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_invite_not_found(async_client: AsyncClient):
    response = await async_client.get("/invites/999999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_and_get_invite_success(async_client: AsyncClient, admin_token):
    # Create invite
    create_resp = await async_client.post(
        "/invites/",
        json={"email": "verify@example.com"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert "token" in created
    assert created["email"] == "verify@example.com"

    # Get invite by ID
    invite_id = created["id"]
    get_resp = await async_client.get(
        f"/invites/{invite_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == invite_id
    assert fetched["email"] == "verify@example.com"

