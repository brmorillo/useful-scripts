@echo off
cd C:\Users\bruno\Documents\GitHub\docker-images
docker-compose down
docker system prune -a -f --volumes
docker-compose up -d