import itertools as it
from pathlib import Path
from typing import List
from ..utils import iter_sample_fast
from ..clip_model import get_photo_features
from .model.photo import Photo
from .model.pivot import Pivot
from .alchemy import alchemy
from ..distance import distance


class DatabaseInitializer:
    def __init__(self):
        alchemy.create_all()
        self.pivots: List[Pivot] = Pivot.query.all()

    def __create_pivots(self):
        features = [get_photo_features(p) for p in iter_sample_fast(
            Path(__file__).joinpath('../static/img').glob('*.jpg'), 20)]
        for f1 in features:
            pivot = Pivot(clip_features=f1)
            for i, f2 in enumerate(features):
                pivot[f'p{i}'] = distance(f1, f2)
            alchemy.session.add(pivot)
            alchemy.session.commit()
        self.pivots = Pivot.query.all()

    def recreate_all(self, limit: int = None):
        print('initializing db')
        alchemy.drop_all()
        alchemy.create_all()
        print('tables created')
        print('creating pivots...')
        self.__create_pivots()
        print('precomputing photos...\n')
        for p in it.islice(Path(__file__).joinpath('../static/img').glob('*.jpg'), limit):
            print('\r' + p.name, end='', flush=True)
            self.insert_photo(p)

    def insert_photo(self, path: Path):
        filename = str(path.resolve())
        features = get_photo_features(path)
        photo = Photo(filename=filename, clip_features=features)
        for i, pivot in enumerate(self.pivots):
            photo[f'p{i}'] = distance(pivot.clip_features, features)
