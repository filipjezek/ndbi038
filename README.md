# M-index

## Frontend

Pro vývoj:

- nutné mít nainstalovaný node.js
- `npm i -g @angular/cli`
- `npm i`

Další příkazy:

- Dev server: `ng serve`
- build: `ng build --prod`

## Backend

- Dev server: `python -m flask run`

Fotky patří do `/backend/static/img`. K jejich předpočítání slouží funkce `init_db` s volitelným parametrem udávajícím kolik fotek předpočítat. `init_db` vytvoří sqlite databázi na lokaci uvedené v `/backend/instance/config.py` - `SQLALCHEMY_DATABASE_URI`, například `sqlite:///instance/ndbi038.db`.
