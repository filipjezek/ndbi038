from backend.app import app
from backend.database.initializer import DatabaseInitializer
from werkzeug.exceptions import NotFound
from .server_api import api
import flask

with app.app_context():
    initializer = DatabaseInitializer()
    # comment this line out if you want to reuse already populated db
    initializer.recreate_all()


app.register_blueprint(api, url_prefix='/api/')


@app.errorhandler(404)
def serve_spa(error: NotFound):
    try:
        return flask.send_from_directory(app.static_folder + '/frontend_dist', flask.request.path[1:])
    except NotFound:
        return app.send_static_file('frontend_dist/index.html')
