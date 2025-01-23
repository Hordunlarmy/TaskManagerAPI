#!/bin/sh

# Make and apply migrations
echo "Making migrations..."
python3 manage.py makemigrations

echo "Applying migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Start the Uvicorn server
exec uvicorn core.asgi:application \
	--host 0.0.0.0 \
	--port "$PORT" \
	--timeout-keep-alive 5000 \
	--workers 3
