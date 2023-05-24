from .server_api import api
from .app import app
from .database.initializer import DatabaseInitializer

initializer = DatabaseInitializer()
initializer.recreate_all(100)


app.register_blueprint(api, url_prefix='/api/')
