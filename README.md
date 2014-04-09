Visualize traceroute data 

To use flow:

    $ cd backend/
    $ pip install flask pygeoip 
    $ wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    $ gunzip GeoLiteCity.dat.gz
    $ python app.py
