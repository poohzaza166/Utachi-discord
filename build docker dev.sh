pipenv lock -v > requirements.txt

docker build --no-cache -t poohzaza/utachi-discord:latest .