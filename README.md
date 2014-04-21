Visualize traceroute data 

To use flow:

    $ cd backend/
    $ pip install flask pygeoip 
    $ wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    $ gunzip GeoLiteCity.dat.gz
    $ python app.py

Design Limitations:
+ Scalability vs deployability
    - Current approach is highly extensible, but current backend will not scale well
    - Need for better parallelization
+ Visualization
    - Current library does not support directed edges
        - tools exist for this, but cannot handle our data
    - Geolocation limited by GeoIP database
+ Analysis
    - Current tool gives data visualization, not analysis
    - Could augment with heuristics to flag interesting behavior
