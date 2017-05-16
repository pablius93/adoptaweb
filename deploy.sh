cat docs/info/docker.txt

echo "Collecting static files"
python manage.py collectstatic

docker-compose up
