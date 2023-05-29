from flask import Flask
from flask_cors import CORS
from pathlib import Path
import os

app = Flask(
    __name__,
    instance_relative_config=True,
    instance_path=Path(__file__).joinpath('../instance').resolve(),
    root_path=Path(__file__).joinpath('..').resolve(),
    static_url_path='/',
    static_folder=Path(__file__).joinpath('../static').resolve(),
)


# Load the default configuration
app.config.from_object('config.default')
if 'NDBI038_MODE' in os.environ and os.environ['NDBI038_MODE'] == 'prod':
    app.config.from_object('config.production')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

cors = CORS(app)
