import pytest
import json
import asyncio

from httpx import AsyncClient, ASGITransport
from datetime import timedelta
from sqlalchemy.orm import Session

from main import app
from api.common.crypto import get_private_key
from core.utils.crypto.rsa import RSA
from core.utils.token import create_token
from database import engineconn, set_engine


# JWT 토큰 생성
access_token = create_token({"sub": "test@example.com"}, expires_delta=timedelta(minutes=15))
expired_token = create_token({"sub": "test@example.com"}, expires_delta=timedelta(minutes=-1))
invalid_token = "invalid.token.payload"

headers = {"Authorization": f"Bearer {access_token}"}
expired_headers = {"Authorization": f"Bearer {expired_token}"}
invalid_headers = {"Authorization": "Bearer {invalid_token}"}
no_headers = {}

engine = engineconn("127.0.0.1")
set_engine(engine)

existed_shorturl = None

def get_session():
    session = engine.sessionmaker()
    return session


def parse_resp(resp, expected):
    assert resp["header"]["code"] in expected
    return resp


def encrypt_password(password, certificate_id):
    session = get_session()
    private_key = get_private_key(session, certificate_id)
    return RSA.encrypt(private_key, password)

def test_register_user():

    async def __test_register_user_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            certificate_id = 1
            response = await client.post('/api/user/v1/register', json={'body': {'certificate_id': certificate_id, 'email': 'test@example.com', 'password': encrypt_password('encrypted_password', certificate_id)}})
        parse_resp(response.json(), [0, -10001])
    asyncio.run(__test_register_user_inner())

def test_register_duplicate_user():

    async def __test_register_duplicate_user_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            certificate_id = 1
            response = await client.post('/api/user/v1/register', json={'body': {'certificate_id': certificate_id, 'email': 'test@example.com', 'password': encrypt_password('encrypted_password', certificate_id)}})
        parse_resp(response.json(), [-10001])
    asyncio.run(__test_register_duplicate_user_inner())

def test_login():

    async def __test_login_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            certificate_id = 1
            response = await client.post('/api/auth/v1/login', json={'body': {'certificate_id': certificate_id, 'email': 'test@example.com', 'password': encrypt_password('encrypted_password', certificate_id)}})
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data['body']['token']
        assert 'refresh_token' in data['body']['token']
    asyncio.run(__test_login_inner())

def test_login_invalid_password():

    async def __test_login_invalid_password_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            certificate_id = 1
            response = await client.post('/api/auth/v1/login', json={'body': {'certificate_id': certificate_id, 'email': 'test@example.com', 'password': encrypt_password('encrypted_password1', certificate_id)}})
        parse_resp(response.json(), [-10004])
    asyncio.run(__test_login_invalid_password_inner())

def test_create_shorturl():

    async def __test_create_shorturl_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {'source': 'https://example.com'}}, headers=headers)
        global existed_shorturl
        global first_shorturl
        body = response.json()['body']
        existed_shorturl = body['shorturl']['shorturl']
        first_shorturl = body['shorturl']['shorturl']
        assert response.status_code == 200
        assert 'shorturl' in body
    asyncio.run(__test_create_shorturl_inner())

def test_create_shorturl_with_invalid_access_token():

    async def __test_create_shorturl_with_invalid_access_token_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {'source': 'https://example.com'}}, headers=invalid_headers)
        body = response.json()['body']
        assert response.status_code == 500
    asyncio.run(__test_create_shorturl_with_invalid_access_token_inner())

def test_create_shorturl_with_expired_access_token():

    async def __test_create_shorturl_with_expired_access_token_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {'source': 'https://example.com'}}, headers=expired_headers)
        body = response.json()['body']
        assert response.status_code == 401
    asyncio.run(__test_create_shorturl_with_expired_access_token_inner())

def test_create_shorturl_with_no_access_token():

    async def __test_create_shorturl_with_no_access_token_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {'source': 'https://example.com'}}, headers=no_headers)
        body = response.json()['body']
        assert response.status_code == 500
    asyncio.run(__test_create_shorturl_with_no_access_token_inner())

def test_create_shorturl_make_diffrent_even_the_sameurl():

    async def __test_create_shorturl_make_diffrent_even_the_sameurl_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {'source': 'https://example.com'}}, headers=headers)
        body = response.json()['body']
        assert response.status_code == 200
        assert first_shorturl != body['shorturl']['shorturl']
    asyncio.run(__test_create_shorturl_make_diffrent_even_the_sameurl_inner())

def test_create_shorturl_invalid_url():

    async def __test_create_shorturl_invalid_url_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.post('/api/shorturl/v1/shorturl', json={'body': {}}, headers=headers)
        global existed_shorturl
        assert response.status_code == 500
    asyncio.run(__test_create_shorturl_invalid_url_inner())

def test_visit_existing_shorturl():

    async def __test_visit_existing_shorturl_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.get(f'/api/shorturl/v1/shorturl/{existed_shorturl}')
        assert response.status_code == 200
    asyncio.run(__test_visit_existing_shorturl_inner())

def test_visit_nonexistent_shorturl():

    async def __test_visit_nonexistent_shorturl_inner():
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            response = await client.get('/api/shorturl/v1/shorturl/nonexistent')
        assert response.status_code == 404
    asyncio.run(__test_visit_nonexistent_shorturl_inner())

