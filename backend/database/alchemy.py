from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator
from sqlalchemy import types
import io
import numpy as np
from backend import app

alchemy = SQLAlchemy(app)


class NumpyArray(TypeDecorator):
    impl = types.LargeBinary

    def process_bind_param(self, value, dialect):
        out = io.BytesIO()
        np.save(out, value)
        out.seek(0)
        return out.read()

    def process_result_value(self, value, dialect):
        out = io.BytesIO(value)
        out.seek(0)
        return np.load(out)
