import sqlalchemy as sql
from sqlalchemy import types
from backend.database.model.pivot import PIVOT_COUNT
from backend.database.alchemy import alchemy, NumpyArray


class Photo(alchemy.Model):
    id = sql.Column(types.Integer, primary_key=True)
    key = sql.Column(types.Double, index=True, nullable=False)
    filename = sql.Column(types.String, unique=True, nullable=False)
    clip_features = sql.Column(NumpyArray, nullable=False)


for i in range(PIVOT_COUNT):
    setattr(Photo, f'p{i}', sql.Column(types.Float, nullable=False))
