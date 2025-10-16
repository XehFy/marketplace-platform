import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from auth.main import app

from httpx import ASGITransport

@pytest.mark.asyncio
async def test_ping():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
