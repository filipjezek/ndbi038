# M-index

This is an implementation of metric index for similarity search in photos. Most of the
theory is based on this work: <https://www.sciencedirect.com/science/article/pii/S0306437910001109>.
The main part of the application is implemented as a python flask server. The frontend is a simple
Angular web app, and its only purpose is some kind of GUI to test the index.

Image features are extracted using [OpenAI CLIP](https://openai.com/research/clip), which also
allows us to search using text input.

## Frontend

All commands should be executed in the `/frontend` folder.

### Environment

- Node.js 18
- `npm i`

### Other commands

- Dev server: `npm run start` (by default localhost:4200)
- build: `npm run build` (this builds the site and puts it into the flask static folder)

### Usage

It is possible to specify either text or image query. The results will be displayed based on the selected
display type. The amount of results can also be specified, but it will be rounded up so that the whole
result grid will be filled.

## Backend

All commands should be executed in the `/backend` folder.

- Python 3.11
- `pip install -r requirements.txt`
- server: `python -m flask run` (by default localhost:5000)

The photos belong to `/backend/static/img`. You should specify your own `/backend/instance/config.py` - there is
a sample provided.

### Structure

Most of the metrc index work is done in a static class `ClusterTree`. There, each photo is assigned its hash. The
hashes are indexed in a sqlite file (which is initialized in `DatabaseInitializer`).
