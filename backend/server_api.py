import flask
from backend.cluster_tree import ClusterTree
from backend.clip_model import get_photo_features, get_text_features
from backend.utils import data_url_to_image
from backend.display import triangle, DisplayTypes, get_filename
from timeit import default_timer

api = flask.Blueprint("api", __name__)


@api.route('query', methods=['POST'])
def post_query():
    try:
        body = flask.request.get_json()
        assert 'text' in body or 'image' in body
        width = int(body['width'])
        height = int(body['height'])
        d_type = DisplayTypes(body['displayType'])
    except:
        return flask.Response(status=400)
    # start = default_timer()
    if 'text' in body:
        features = get_text_features(body['text'])
    else:
        features = get_photo_features(data_url_to_image(body['image']))
    # start = print_progress(start, 'features extracted')

    res = ClusterTree.knn_search(features, width * height)
    # start = print_progress(start, 'search finished')
    res = [get_filename(p.filename)
           for p in res]
    # start = print_progress(start, 'filenames extracted')
    if d_type == DisplayTypes.triangle:
        res = triangle(res, width, height)
    return flask.jsonify(res)


def print_progress(prev_time: float, label: str):
    now = default_timer()
    print(f'[+{now - prev_time}s]', label)
    return now
