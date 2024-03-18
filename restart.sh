docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force
docker-compose up --build --force-recreate --no-deps
