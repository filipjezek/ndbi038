import sqlalchemy as sql
from sqlalchemy import types
from .pivot import PIVOT_COUNT
from ..alchemy import alchemy, NumpyArray


class Photo(alchemy.Model):
    key = sql.Column(types.Float, primary_key=True, autoincrement=False)
    filename = sql.Column(types.String, unique=True, nullable=False)
    clip_features = sql.Column(NumpyArray, nullable=False)


for i in range(PIVOT_COUNT):
    Photo[f'p{i}'] = sql.Column(types.Float, nullable=False)
