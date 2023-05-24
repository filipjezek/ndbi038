from .app import app
from .database.initializer import DatabaseInitializer

with app.app_context():
    initializer = DatabaseInitializer()
    initializer.recreate_all(100)

from .server_api import api  # nopep8

app.register_blueprint(api, url_prefix='/api/')
