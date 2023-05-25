import itertools as it
from pathlib import Path
from typing import List
from sqlalchemy import select
from backend.utils import iter_sample_fast
from backend.clip_model import get_photo_features
from backend.database.model.photo import Photo
from backend.database.model.pivot import Pivot
from backend.database.alchemy import alchemy
from backend.distance import distance
from backend.cluster_tree import ClusterTree


class DatabaseInitializer:
    def __init__(self):
        alchemy.create_all()
        self.pivots: List[Pivot] = list(alchemy.session.execute(
            select(Pivot)).scalars())
        print('rebuilding tree...')
        ClusterTree.reset(self.pivots)
        for obj in alchemy.session.execute(select(Photo)).scalars():
            ClusterTree.insert_object(obj)

    def __create_pivots(self):
        features = [get_photo_features(p) for p in iter_sample_fast(
            Path(__file__).joinpath('../../static/img').glob('*.jpg'), 20)]
        for f1 in features:
            pivot = Pivot(clip_features=f1)
            for i, f2 in enumerate(features):
                setattr(pivot, f'p{i}', distance(f1, f2))
            alchemy.session.add(pivot)
            alchemy.session.commit()
        self.pivots = list(alchemy.session.execute(
            select(Pivot)).scalars())

    def recreate_all(self, limit: int = None):
        print('initializing db')
        alchemy.session.close()
        alchemy.drop_all()
        alchemy.create_all()
        print('tables created')
        print('creating pivots...')
        self.__create_pivots()
        ClusterTree.reset(self.pivots)
        print('precomputing photos...')
        for p in it.islice(Path(__file__).joinpath('../../static/img').glob('*.jpg'), limit):
            print('\r' + p.name, end='', flush=True)
            self.insert_photo(p)
        print('\nready')

    def insert_photo(self, path: Path):
        filename = str(path.resolve())
        features = get_photo_features(path)
        photo = Photo(filename=filename, clip_features=features)
        for i, pivot in enumerate(self.pivots):
            setattr(photo, f'p{i}', distance(pivot.clip_features, features))
        ClusterTree.insert_object(photo)
        alchemy.session.add(photo)
        alchemy.session.commit()
