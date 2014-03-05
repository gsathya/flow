Visualize traceroute data 


To use the frontend:

    $ cd frontend/
    $ python -m SimpleHTTPServer

To use the backend:

    $ cd backend/
    $ pip install flask pygeoip 
    $ wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    $ gunzip GeoLiteCity.dat.gz
    $ python app.py
