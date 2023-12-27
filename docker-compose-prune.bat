cd %USERPROFILE%\github\wallet-docker-images
docker-compose down
docker system prune -a -f --volumes
docker-compose up -d