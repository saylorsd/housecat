#!/usr/bin/env bash

# Apply database migrations
echo "Apply database migrations"
./bin/wait-for-it.sh -t 5 db:5432 -- echo "✅ DB is up"
./bin/wait-for-it.sh -t 5 datastore-db:5432 -- echo "✅ Datastore DB is up"

COUNTER=0

while
  ./manage.py migrate --noinput
  M=$?
  [[ $M -eq 1 ]] && [ $COUNTER -lt 6 ]
do
  ((COUNTER++))
  echo "⚠️ couldn't migrate, trying again shortly"
  echo "    (attempt $COUNTER of 5)"
  sleep 3
done

echo "🧑‍💻 Creating superuser"
./manage.py createsuperuser --noinput

echo "📡 Connecting to CKAN datastore"
./manage.py connect_datastore

echo "🚛 Collecting Housing Data"
./manage.py connect_housing_data

if [[ -v $MANAGE_DATASTORE ]]; then
  echo "🧪🗄️ Generating Dummy Data"
  ./manage.py generate_dummy_data
fi

echo "📦 Collecting static files"
./manage.py collectstatic --noinput

echo "🆙 Starting..."
./manage.py runserver 0.0.0.0:8000

exec "$@"
