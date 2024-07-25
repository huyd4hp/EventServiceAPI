docker stop api.event api.sevent EventService
docker rm api.event api.sevent EventService
docker build -t event-service .
docker compose -f service.yaml up -d