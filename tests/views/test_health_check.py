from httpx import AsyncClient


async def test_ping_application(client: AsyncClient):
    response = await client.get('/health_check/ping_application')
    assert response.status_code == 200
    assert response.json() == {'message': 'Pong'}


async def test_ping_database(client: AsyncClient):
    response = await client.get('/health_check/ping_database')
    assert response.status_code == 200
    assert response.json() == {'message': 'Pong'}
