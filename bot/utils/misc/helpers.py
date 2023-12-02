import aiohttp

from utils import new_redis_conn


async def is_authenticated_check(user_id):
    with new_redis_conn() as client:
        token = client.get(f'{user_id}')
        if not token:
            return False
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token.decode("utf-8")}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:9999/users/me', headers=headers) as response:
                return True if response.status == 200 else False

