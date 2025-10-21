import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from services.auth.routes import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_register_new_user():
    mock_get_user_by_email = AsyncMock(return_value=None)
    mock_create_user = AsyncMock(return_value={
        "id": 1,
        "email": "test@example.com",
        "is_active": True
    })
    mock_hash_password = AsyncMock(return_value="hashed123")

    with patch("services.auth.routes.get_user_by_email", mock_get_user_by_email), \
         patch("services.auth.routes.create_user", mock_create_user), \
         patch("services.auth.routes.hash_password", mock_hash_password):

        with TestClient(app) as client:
            response = client.post("/auth/register", json={
                "email": "test@example.com",
                "password": "secret123"
            })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == 1
    assert data["is_active"] is True
    mock_create_user.assert_awaited_once()
    mock_get_user_by_email.assert_awaited_once()
