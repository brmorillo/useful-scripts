cd %USERPROFILE%\github\docker-images
docker-compose down
docker system prune -a -f --volumes
docker-compose up -d