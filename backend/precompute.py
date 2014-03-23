#! /usr/bin/python
# Ben Jones
# Spring 2014
# 6675 Traceroute visualization project
#
# precompute: module to precompute the prevalence and persistence of
# internet paths from the traceroute data and output the computation
# to a new db

import cPickle
import dbhash
from scipy import stats
import sqlite3

def precompute_monthly_db(inputFilename, outputFilename):
    """Compute the average prevalence, persistence, and rtt for each hop
    on each path between unique start and end points

    Parameters:

    inputFilename: the name of the monthly data file. This will be a
    Berkeley DB

    outputFilename: the name of the expected output file. This will
    use sqlite

    Note: a path is defined between a unique start and end point. In
    the context of this module, a path is the unique start-end point
    combination of a BISmark router and an M-Lab server

    """
    get_groups = ("SELECT sub.hop, sub.deviceid, sub.eventstamp, sub.ip, sub.rtt "
                  "FROM traceroute sub, traceroute prev WHERE prev.ip = ? "
                  "AND prev.hop = ? and sub.hop = ? AND sub.toolid= 'paris-traceroute' "
                  "AND prev.eventstamp = sub.eventstamp ORDER BY sub.ip, sub.eventstamp ")
    get_persistence_data = ("SELECT sub.ip, sub.eventstamp FROM traceroute sub, "
                            "traceroute prev WHERE prev.ip = ? AND prev.hop = ? "
                            "AND sub.hop = ? AND sub.toolid = 'paris-traceroute' AND "
                            "prev.eventstamp = sub.eventstamp ORDER BY sub.eventstamp")
    insert_data = ("INSERT into monthlyData (deviceid, srcip, dstip, hop, vertex_ip1, "
                   "vertex_ip2, avg_rtt real, prevalence real, persistence real) VALUES "
                   "(%(deviceid)s, %(srcip)s, %(dstip)s, %(hop)s, %(vertex_ip1)s, "
                   "%(vertex_ip2)s, %(avg_rtt)s, %(prevalence)s, %(persistence)s)")
    # setup the database connections
    # db = dbhash.open(inputFilename)
    db = sqlite3.connect(inputFilename)
    outputDB = sqlite3.connect(outputFilename)
    cursor = db.cursor()

    # iterate over all unique paths
    cursor.execute("SELECT distinct srcip from traceroute")
    srcIPs = cursor.fetchall()
    cursor.execute("SELECT distinct dstip from traceroute")
    destIPs = cursor.fetchall()
    print "starting up"
    for (start,) in srcIPs:
        for (dest,) in destIPs:
            print "Starting path {} {}".format(start, dest)
            # get all the distinct hops as a first step to getting all
            # the previous ips
            cursor.execute("SELECT MAX(hop) from traceroute WHERE srcip = ? and dstip = ?", (start, dest))
            (maxHops,) = cursor.fetchone()
            for hop in range(maxHops):
                print "Starting hop {} for path {} to {}".format(hop, start, dest)
                cursor.execute("SELECT distinct ip from traceroute WHERE srcip = ? AND dstip= ? AND hop = ?",(start, dest, hop))
                prevHopIPs = [ip for (ip,) in cursor.fetchall()]
                for prevHopIP in prevHopIPs:
                # for each hop, find all of the next hops
                    cursor.execute(get_groups, (prevHopIP, hop, hop+1))
                    # get the data for all of the subsequent IPs
                    rtts = []
                    info = []
                    rttGroup = None
                    prevIP = ""
                    prevHop = -1
                    totalElems = 0
                    for (hop, router, eventstamp, ip, rtt) in cursor.fetchall():
                        if hop != prevHop or prevIP != ip:
                            prevHop = hop
                            prevIP = ip
                            if rttGroup != None:
                                rtts.append(rttGroup)
                                info.append({'hop':hop, 'router':router, 'vertex_ip1':prevHopIP, 
                                             'vertex_ip2':ip, 'srcip':start, 'dstip':dest})
                            rttGroup = [rtt]
                        else:
                            rttGroup.append(rtt)
                        totalElems += 1
                    # for each group, find the avg rtt
                    toInsert = []
                    for index in range(len(rtts)):
                        avgRtt = stats.nanmean(rtts[index])
                        info[index]['avg_rtt'] = avgRtt
                        prevalence = float(len(rtts[index])) / float(totalElems)
                        info[index]['prevalence'] = prevalence
                        toInsert.append(info[index])
                    cursor.execute(get_persistence_data, (prevIP, hop, hop+1))
                    data = cursor.fetchall()
                    for index in range(len(toInsert)):
                        testIP = toInsert[index]['vertex_ip2']
                        runs = []
                        startEventstamp = data[0][0]
                        inPrevRun = False
                        curEventstamp = data[0][0]
                        seenIP = False
                        for (ip, eventstamp) in data:
                            if eventstamp != curEventstamp:
                                if seenIP == True:
                                    if inPrevRun == False:
                                        startEventstamp = eventstamp
                                else:
                                    # if there is a run to compute, then compute it
                                    if inPrevRun == True:
                                        runs.append(curEventstamp -startEventstamp)
                                    inPrevRun = False
                                curEventstamp = eventstamp
                                seenIP = False
                            if ip == testIP:
                                seenIP = True
                        persistence = stats.nanmean(runs)
                        toInsert[index]['persistence'] = persistence
                        cursor.execute(insert_data, toInsert[index])

def create_table(filename):
    outputDB = sqlite3.connect(filename)
    create_table_query = ("CREATE TABLE monthlyData (deviceid text, srcip text, dstip text, hop integer, vertex_ip1 text, vertex_ip2 text, avg_rtt real, prevalence real, persistence real)")
    outputDB.execute(create_table_query)
    outputDB.commit()
    outputDB.close()

if __name__ == "__main__":
#    create_table('monthly-data.db')
    precompute_monthly_db('sqlite-traceroute-data.db', 'monthly-data.db')
