from multiprocessing.connection import Connection
from fastapi import FastAPI, status, Response
import databases
import db
import geoapi
from pydantic import BaseModel, ValidationError
from dot import Dot
from multiprocessing import Process, Pipe
from coord import *

app = FastAPI()
geo = geoapi.GeoApiProvider()

database = databases.Database('sqlite+aiosqlite:///cities.db')

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.get('/')
async def root():
    return { 'message': 'hello world'}

@app.delete('/city/{name}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(name: str, response: Response):
    query = db.cities.delete().where(db.cities.c.name==name)

    rows = await database.execute(query)

    if rows == 0:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.post('/city/{name}', status_code=status.HTTP_201_CREATED)
async def post_city(name: str):
    coord = await geo.coordinates_by_name(name)
    query = db.cities.insert().values(name=name, lat=coord[0], lon=coord[1])

    await database.execute(query)

    return { 'name': name }

@app.get('/city/{name}')
async def get_city(name: str, response: Response):
    query = db.cities.select().where(db.cities.c.name==name)

    city = await database.fetch_one(query)

    if city is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return city

@app.get('/coord')
async def get_nearest_cities(lat: float, lon: float):
    query = db.cities.select()
    cities = await database.fetch_all(query)

    dot = Coordinate((lat, lon))

    rx, tx = Pipe()
    proc = Process(target=get_city_distance, args=(dot, cities, tx))

    proc.start()

    cities = rx.recv()

    proc.join()

    return cities



def get_city_distance(dot: Coordinate, cities: list[tuple[int, str, float, float]], tx: Connection) -> tuple[str, float]:
    cities_distances = []
    for city in cities:
        city_coord = Coordinate(city[2:])
        dist = distance(dot, city_coord)
        cities_distances.append((city[1], dist))

    cities_distances.sort(key=lambda x: x[1])

    tx.send(cities_distances[:2])
