# M-index

Příkazy pro backend a frontend jsou nutné spouštět v daných složkách

## Frontend

Pro vývoj:

- nutné mít nainstalovaný node.js
- `npm i`

Další příkazy:

- Dev server: `npm run start`
- build: `npm run build` (aplikace pak běží čistě přes flask server)

## Backend

- Python 3.11
- server: `python -m flask run`

Fotky patří do `/backend/static/img`. K jejich předpočítání slouží funkce `init_db` s volitelným parametrem udávajícím kolik fotek předpočítat. `init_db` vytvoří sqlite databázi na lokaci uvedené v `/backend/instance/config.py` - `SQLALCHEMY_DATABASE_URI`, například `sqlite:///ndbi038.db`.
