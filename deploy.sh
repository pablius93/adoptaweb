cat docs/info/docker.txt

sh scripts/compile_react.sh

echo "Collecting static files"
python manage.py collectstatic

docker-compose up
