#! /usr/bin/env bash

# Let the DB start
python3 ./app/backend_prestart.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python3 ./app/initial_data.py