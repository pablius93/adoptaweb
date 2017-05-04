cat docs/info/docker.txt

echo "Starting docker db container"
docker-compose -f docker-compose.dev.yml start

echo "Starting development server"
python3.5 manage.py runserver 0.0.0.0:8000 &

cd client/
echo "Starting client app"
npm start > /dev/null 2>&1
