# FastSAM API setup

Reference: https://github.com/CASIA-IVA-Lab/FastSAM

SAM-API (with CPU only)

```
cd backend
docker build -t sam-api .
docker run -p 4000:4000 sam-api
```

Run frontend server

```
cd frontend
docker build -t frontend-server .
docker run --net=host frontend-server

open browser and open http://127.0.0.1:5000/
```

Networking issue

```
--net=host will host the container under host network
```
