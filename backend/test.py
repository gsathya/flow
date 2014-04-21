import sqlite3
import pygeoip
import json
import sys
from sets import Set

def testfn():
    
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    query = "SELECT * FROM monthlyData where deviceid=\"744401936B2E\""
    
    conn = sqlite3.connect('../data/monthlystats.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print row        

def main():
    testfn()

if __name__=="__main__":
    main()
