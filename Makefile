include .env

local:
	uvicorn app.main:app --reload --host ${APP_HOST} --port ${APP_PORT}

test:
	pytest --disable-warnings --asyncio-mode=auto -vv -x -rP

lint:
	flake8 app --count --exit-zero --exclude=app/db/migrations/ --max-complexity=10 --max-line-length=127 --statistics
	flake8 tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .
	unify --in-place --recursive --quote "'" .

docker-up:
	docker-compose --env-file .env up -d --build

docker-down:
	docker-compose down

env:
	cp .env.example .env

db-up:
	docker-compose --env-file .env up -d db

db-down:
	docker-compose stop db
	docker-compose rm -f db

