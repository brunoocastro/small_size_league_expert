api:
	uv run fastapi run api.py --port 3000 --reload

discord:
	uv run python discord_bot.py

watch:
	docker compose watch

up:
	docker compose up -d

down:
	docker compose down