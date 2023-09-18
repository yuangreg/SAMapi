requirements.txt is obtained from pip freeze --local > requirements.txt in the venv.

Please run the frontend and backend dockerfiles following the readme.txt in the respective folders.

Check using docker ps. There should be 2 containers running, with image sam-api and frontend-server, respectively.

use http://localhost:5000/ to start the frontend server, which will interact with the backend server.
