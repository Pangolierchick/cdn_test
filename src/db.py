import sqlalchemy

metadata = sqlalchemy.MetaData()

cities = sqlalchemy.Table(
    'cities',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('lat', sqlalchemy.Float),
    sqlalchemy.Column('lon', sqlalchemy.Float)
)
