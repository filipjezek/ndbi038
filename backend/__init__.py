from backend.app import app
from backend.database.initializer import DatabaseInitializer

with app.app_context():
    initializer = DatabaseInitializer()
    initializer.recreate_all()

from .server_api import api  # nopep8

app.register_blueprint(api, url_prefix='/api/')
