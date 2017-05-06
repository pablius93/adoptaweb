cat docs/info/docker.txt

source env/dev/bin/activate
echo "Starting docker db container"
docker-compose -f docker-compose.dev.yml start

echo "Starting development server"
python3.5 manage.py runserver 0.0.0.0:8000
