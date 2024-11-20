# Correrlo
docker build -t election model .
docker run --rm -it election-model

# O usando docker-compose:
docker-compose up --build
