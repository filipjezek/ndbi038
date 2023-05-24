import sqlalchemy as sql
from sqlalchemy import types
from ..alchemy import alchemy, NumpyArray


PIVOT_COUNT = 20


class Pivot(alchemy.Model):
    id = sql.Column(types.Integer, primary_key=True)
    clip_features = sql.Column(NumpyArray, nullable=False)


for i in range(PIVOT_COUNT):
    setattr(Pivot, f'p{i}', sql.Column(types.Float, nullable=False))
