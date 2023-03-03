pipenv lock -r > requirements.txt
docker build --no-cache -t poohzaza/utachi-discord:latest .