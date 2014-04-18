import sqlite3
import pygeoip
import json
import sys
from sets import Set

def is_private(address):
    """
        Checks if the IPv4 address is in a range belonging to the local network or
        loopback. These include:
        
        * Private ranges: 10.*, 172.16.* - 172.31.*, 192.168.*
        * Loopback: 127.*
        """
    
    # checks for any of the simple wildcard ranges
    if address.startswith("10.") or address.startswith("192.168.") or address.startswith("127."):
        return True
    
    # checks for the 172.16.* - 172.31.* range
    if address.startswith("172."):
        second_octet = int(address.split('.')[1])
        
        if second_octet >= 16 and second_octet <= 31:
            return True
    
    return False

def getsqlite(filename, query):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    conn = sqlite3.connect('../data/' + filename)
    conn.row_factory = sqlite3.Row
    
    cur = conn.cursor()
    
    cur.execute(query)
    
    rows = cur.fetchall()
    
    paths = []
    path = []
    dest = None
    
    for row in rows:
        # new path
        if row["hop"] == 1:
            # add prev path to our list
            if path:
                # dest should be added at the end
                if dest and path[-1] != dest:
                    path.append(dest)
                    dest = None
                
                paths.append(path)
            ip_info = gi.record_by_addr(row["srcip"])
            path = [(ip_info["latitude"], ip_info["longitude"])]
        
        ip = row["ip"]
        
        if is_private(ip) or ip == "*":
            continue
        
        ip_info = gi.record_by_addr(ip)
        lat, lang = ip_info["latitude"], ip_info["longitude"]
        
        if path[-1] != (lat, lang):
            path.append((lat, lang))
        
        if not dest:
            ip_info = gi.record_by_addr(ip)
            lat, lang = ip_info["latitude"], ip_info["longitude"]
            dest = (lat, lang)
    
    # add final path that we missed
    if path:
        if dest and path[-1] != dest:
            path.append(dest)
        paths.append(path)
    
    conn.close()
    
    data = {'paths': paths}
    
    return data

def getmonthlystats(srcip, dstip):
    
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    query = "SELECT * FROM monthlyData WHERE srcip=\"" + str(srcip) + "\" AND dstip=\"" + str(dstip) + "\""
    print "Query: " + query
    
    conn = sqlite3.connect('../data/monthlystats.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    result = {}
    avg_rtt = []
    prevalence = []
    persistence = []
    vertex_ip1_lat = []
    vertex_ip1_lng = []
    vertex_ip2_lat = []
    vertex_ip2_lng = []
    hop = []
    
    srcloc = gi.record_by_addr(srcip)
    dstloc = gi.record_by_addr(dstip)
    result["srclat"] = srcloc['latitude']
    result["srclng"] = srcloc['longitude']
    result["dstlat"] = dstloc['latitude']
    result["dstlng"] = dstloc['longitude']
    
    for row in rows:
        avg_rtt.append(row["avg_rtt"])
        prevalence.append(row["prevalence"])
        persistence.append(row["persistence"])
        hop.append(row["hop"])
        if is_private(row["vertex_ip1"]):
            ip1_loc = srcloc
        else:
            ip1_loc = gi.record_by_addr(row["vertex_ip1"])
        if is_private(row["vertex_ip2"]):
            ip2_loc = srcloc
        else:
            ip2_loc = gi.record_by_addr(row["vertex_ip2"])
        vertex_ip1_lat.append(ip1_loc['latitude'])
        vertex_ip1_lng.append(ip1_loc['longitude'])
        vertex_ip2_lat.append(ip2_loc['latitude'])
        vertex_ip2_lng.append(ip2_loc['longitude'])
    
    result["vertex_ip1_lat"] = vertex_ip1_lat
    result["vertex_ip1_lng"] = vertex_ip1_lng
    result["vertex_ip2_lat"] = vertex_ip2_lat
    result["vertex_ip2_lng"] = vertex_ip2_lng
    result["avg_rtt"] = avg_rtt
    result["prevalence"] = prevalence
    result["persistence"] = persistence
    result["hop"] = hop
    
    return result

def getmonthlystatsforsrcip(srcip):
    
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    query = "SELECT * FROM monthlyData WHERE srcip=\"" + str(srcip) + "\" ORDER BY hop ASC"
    
    conn = sqlite3.connect('../data/monthlystats.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    result = {}    

    visited = set()
    
    srcloc = gi.record_by_addr(srcip)
    srcLat = srcloc['latitude']
    srcLng = srcloc['longitude']

    for rowOut in rows:

        currentDst = rowOut["dstip"]

        if currentDst in visited:
            continue
        visited.add(currentDst)

        dstloc = gi.record_by_addr(currentDst)
        dstLat = dstloc['latitude']
        dstLng = dstloc['longitude']

        record = {}
        avg_rtt = []
        prevalence = []
        persistence = []
        vertex_ip1_lat = []
        vertex_ip1_lng = []
        vertex_ip2_lat = []
        vertex_ip2_lng = []
        hopCount = 0
        prevhop = 0

        for row in rows:
            dstip = row["dstip"]
            if dstip != currentDst:
                continue
            curhop = row["hop"]
            vertex_ip1 = row["vertex_ip1"]
            vertex_ip2 = row["vertex_ip2"]
            if is_private(vertex_ip1):
                ip1_loc = srcloc
            else:
                ip1_loc = gi.record_by_addr(vertex_ip1)
            if is_private(vertex_ip2):
                ip2_loc = dstloc
            else:
                ip2_loc = gi.record_by_addr(vertex_ip2)
            # Missing hop
            if curhop > prevhop + 1:
                # At the beginning
                if prevhop == 0:
                    vertex_ip1_lat.append(srcLat)
                    vertex_ip1_lng.append(srcLng)
                # Somewhere in the middle
                else:
                    vertex_ip1_lat.append(vertex_ip2_lat[-1])
                    vertex_ip1_lng.append(vertex_ip2_lng[-1])
                vertex_ip2_lat.append(ip1_loc['latitude'])
                vertex_ip2_lng.append(ip1_loc['longitude'])                                
                avg_rtt.append('n/a')
                prevalence.append('n/a')
                persistence.append('n/a')
                hopCount = hopCount + 1
                prevhop = curhop
            # This hop's vertices
            vertex_ip1_lat.append(ip1_loc['latitude'])
            vertex_ip1_lng.append(ip1_loc['longitude'])
            vertex_ip2_lat.append(ip2_loc['latitude'])
            vertex_ip2_lng.append(ip2_loc['longitude'])
            avg_rtt.append(row["avg_rtt"])
            prevalence.append(row["prevalence"])
            persistence.append(row["persistence"])
            hopCount = hopCount + 1
            prevhop = curhop

        # Final hop is missing
        if vertex_ip2_lat[-1] != dstLat or vertex_ip2_lng[-1] != dstLng:
            vertex_ip1_lat.append(vertex_ip2_lat[-1])
            vertex_ip1_lng.append(vertex_ip2_lng[-1])
            vertex_ip2_lat.append(dstLat)
            vertex_ip2_lng.append(dstLng)
            avg_rtt.append('n/a')
            prevalence.append('n/a')
            persistence.append('n/a')
            hopCount = hopCount + 1

        record["dstLat"] = dstloc['latitude']
        record["dstLng"] = dstloc['longitude']
        record["avg_rtt"] = avg_rtt
        record["prevalence"] = prevalence
        record["persistence"] = persistence            
        record["vertex_ip1_lat"] = vertex_ip1_lat
        record["vertex_ip1_lng"] = vertex_ip1_lng
        record["vertex_ip2_lat"] = vertex_ip2_lat
        record["vertex_ip2_lng"] = vertex_ip2_lng
        record["hopCount"] = hopCount

        result[currentDst] = record
    
    return result

def getmonthlystatsformac(mac):
   
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    query = "SELECT * FROM monthlyData WHERE deviceid=\"" + str(mac) + "\""
    print "Query: " + query
    
    conn = sqlite3.connect('../data/monthlystats.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    finalresult = {}
    
    avg_rtt = []
    prevalence = []
    persistence = []
    hop = []
    vertex_ip1_lat = []
    vertex_ip1_lng = []
    vertex_ip2_lat = []
    vertex_ip2_lng = []
    src_lat = []
    src_lng = []
    dst_lat = []
    dst_lng = []
    
    srcip = ''
    dstip = ''
    srcloc = ''
    dstloc = ''
    counter = 0
    for row in rows:
        tempsrc = row["srcip"]
        tempdst = row["dstip"]
        
        if srcip == '' or dstip == '':
            srcip = tempsrc
            dstip = tempdst
        
        if srcloc == '' or srcip != tempsrc:
            srcloc = gi.record_by_addr(srcip)
        
        if dstloc == '' or dstip != tempdst:
            dstloc = gi.record_by_addr(dstip)
        
        if srcip != tempsrc or dstip != tempdst:
            #for previous src and dst point
            result = {}
            result["srclat"] = srcloc['latitude']
            result["srclng"] = srcloc['longitude']
            result["dstlat"] = dstloc['latitude']
            result["dstlng"] = dstloc['longitude']
            result["avg_rtt"] = avg_rtt
            result["prevalence"] = prevalence
            result["persistence"] = persistence
            result["hop"] = hop
            result["vertex_ip1_lat"] = vertex_ip1_lat
            result["vertex_ip1_lng"] = vertex_ip1_lng
            result["vertex_ip2_lat"] = vertex_ip2_lat
            result["vertex_ip2_lng"] = vertex_ip2_lng
            finalresult[counter] = result
            #reset
            srcip = tempsrc
            dstip = tempdst
            avg_rtt = []
            prevalence = []
            persistence = []
            hop = []
            vertex_ip1_lat = []
            vertex_ip1_lng = []
            vertex_ip2_lat = []
            vertex_ip2_lng = []
            counter += 1
        
        #add values
        avg_rtt.append(row["avg_rtt"])
        prevalence.append(row["prevalence"])
        persistence.append(row["persistence"])
        hop.append(row["hop"])
        if is_private(row["vertex_ip1"]):
            ip1_loc = srcloc
        else:
            ip1_loc = gi.record_by_addr(row["vertex_ip1"])
        if is_private(row["vertex_ip2"]):
            ip2_loc = srcloc
        else:
            ip2_loc = gi.record_by_addr(row["vertex_ip2"])
        vertex_ip1_lat.append(ip1_loc['latitude'])
        vertex_ip1_lng.append(ip1_loc['longitude'])
        vertex_ip2_lat.append(ip2_loc['latitude'])
        vertex_ip2_lng.append(ip2_loc['longitude'])
    
    if counter != 0:
        #for last set of values
        result = {}
        result["srclat"] = srcloc['latitude']
        result["srclng"] = srcloc['longitude']
        result["dstlat"] = dstloc['latitude']
        result["dstlng"] = dstloc['longitude']
        result["avg_rtt"] = avg_rtt
        result["prevalence"] = prevalence
        result["persistence"] = persistence
        result["hop"] = hop
        result["vertex_ip1_lat"] = vertex_ip1_lat
        result["vertex_ip1_lng"] = vertex_ip1_lng
        result["vertex_ip2_lat"] = vertex_ip2_lat
        result["vertex_ip2_lng"] = vertex_ip2_lng
        finalresult[counter] = result
    
    return finalresult

def getmonthlysrc():
    
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    
    query = "SELECT DISTINCT srcip FROM monthlyData"
    conn = sqlite3.connect('../data/monthlystats.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    result = {}
    for row in rows:
        tempset = {}
        srcloc = gi.record_by_addr(row["srcip"])
        tempset["srclat"] = srcloc['latitude']
        tempset["srclng"] = srcloc['longitude']
        result[row["srcip"]] = tempset

    return result

def process_db(query, flag):
    if(flag == "daily"):
        return getsqlite("smalldata.db", query)
    elif(flag == "monthly"):
        return getsqlite("largedata.db", query)
    print "Invalid flag"
    return -1
