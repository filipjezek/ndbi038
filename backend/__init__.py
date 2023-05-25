from backend.app import app
from backend.database.initializer import DatabaseInitializer
from backend.database.alchemy import alchemy
from backend.cluster_tree import ClusterTree
from backend.database.model.photo import Photo
from sqlalchemy import select

with app.app_context():
    initializer = DatabaseInitializer()
    initializer.recreate_all(100)

    photo1 = alchemy.session.execute(
        select(Photo).where(Photo.id == 46)
    ).scalar_one()
    results = ClusterTree.knn_search(photo1.clip_features, 8)
    print(results)


from .server_api import api  # nopep8

app.register_blueprint(api, url_prefix='/api/')
