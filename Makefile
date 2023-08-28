local:
	uvicorn app.main:app --reload --host 0.0.0.0

test:
	pytest --disable-warnings --asyncio-mode=auto -vv -x -rP

lint:
	flake8 app --count --exit-zero --exclude=app/db/migrations/ --max-complexity=10 --max-line-length=127 --statistics
	flake8 tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .
	unify --in-place --recursive --quote "'" .

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
