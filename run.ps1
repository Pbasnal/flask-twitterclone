$env:FLASK_APP="api"
$env:FLASK_ENV="Debug"

flask run #-h 0.0.0.0 -p 8000

# docker rm -f senti 2>&1
# docker build -t senti:latest .
# docker run -it -d -p 8080:5000 --name senti senti
# docker logs -f senti