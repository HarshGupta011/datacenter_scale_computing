 #!/bin/bash

cd flask-tutorial
export FLASK_APP=flaskr
flask init-db
nohup flask run -h 0.0.0.0 &