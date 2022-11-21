import requests
import aiohttp
from dotenv import load_dotenv
import os
import asyncio


class GeoApiProvider():
    api_url = 'https://api.api-ninjas.com/v1/geocoding'
    def __init__(self):
        load_dotenv()

        self.API_KEY = os.getenv('API_KEY')

        if self.API_KEY is None:
            raise Exception('api key in .env file not found')

    async def coordinates_by_name(self, city: str) -> tuple[float, float]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url + f'?city={city}', headers={'X-Api-Key': self.API_KEY}) as response:
                if not response.ok:
                    raise Exception(f'Request failed with code {response.status_code}')
                json = await response.json()
                if len(json) == 0:
                    raise Exception(f'City {city} not found')

                return (json[0]['latitude'], json[0]['longitude'])
