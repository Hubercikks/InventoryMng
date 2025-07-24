import httpx
import pytest
from main import app
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("TEST_USER")
password = os.getenv("TEST_PASSWORD")


@pytest.mark.asyncio
async def test_negative_me():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_negative_login():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response_negative = await ac.post("/auth/login",
    data={"username": "user@example.com", "password": "secret"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
    assert response_negative.status_code == 401


@pytest.mark.asyncio
async def test_positive_login():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response_positive=await ac.post("/auth/login",
        data={"username": f"{username}", "password":f"{password}"},
        headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response_positive.status_code == 200
        json_data = response_positive.json()
        assert "access_token" in  json_data
        token = json_data["access_token"]
        assert json_data["token_type"] == "bearer"
        headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response_positive=await ac.get("/me", headers=headers)
        assert response_positive.status_code == 200



