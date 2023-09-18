docker build -t frontend-server .
docker run --net=host frontend-server

open browser and open http://127.0.0.1:5000/
