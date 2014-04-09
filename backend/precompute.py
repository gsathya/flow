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
from multiprocessing import Pool
import os
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
                  "AND prev.hop = ? and sub.hop = ? AND prev.srcip = sub.srcip "
                  "AND prev.dstip = sub.dstip AND sub.srcip = ? AND sub.dstip = ? "
                  "AND prev.eventstamp = sub.eventstamp ORDER BY sub.eventstamp")
    get_first_hop_groups = ("SELECT sub.hop, sub.deviceid, sub.eventstamp, sub.ip, sub.rtt "
                            "FROM traceroute sub WHERE sub.hop = ? AND srcip = ? AND dstip = ? ORDER BY sub.eventstamp")

    get_persistence_data = ("SELECT sub.ip, sub.eventstamp FROM traceroute sub, "
                            "traceroute prev WHERE prev.ip = ? AND prev.hop = ? "
                            "AND sub.hop = ? AND sub.toolid = 'paris-traceroute' AND "
                            "prev.eventstamp = sub.eventstamp ORDER BY sub.eventstamp")
    insert_data = ("INSERT into monthlyData (deviceid, srcip, dstip, hop, vertex_ip1, "
                   "vertex_ip2, avg_rtt, prevalence, persistence) VALUES "
                   "(?, ?, ?, ?, ?, ?, ?, ?, ?)")

    # setup the database connections
    # db = dbhash.open(inputFilename)
    db = sqlite3.connect(inputFilename)
    outputDB = sqlite3.connect(outputFilename)
    cursor = db.cursor()
    outputCursor = outputDB.cursor()

    # iterate over all unique paths
    cursor.execute("SELECT distinct srcip, dstip from traceroute")
    ips = cursor.fetchall()
    # cursor.execute("SELECT distinct srcip from traceroute")
    # srcIPs = cursor.fetchall()
    # cursor.execute("SELECT distinct dstip from traceroute")
    # destIPs = cursor.fetchall()
    # print "starting up"
    # for (start,) in srcIPs:
    #     for (dest,) in destIPs:
    for (start, dest) in ips:
            print "Starting path {} {}".format(start, dest)
            # get all the distinct hops as a first step to getting all
            # the previous ips
            cursor.execute("SELECT MAX(hop) from traceroute WHERE srcip = ? and dstip = ?", (start, dest))
            (maxHops,) = cursor.fetchone()
            # TODO: fix this so that it correctly gets the first elem
            for hop in range(1, maxHops):
                print "Starting hop {} for path {} to {}".format(hop, start, dest)
                # if this is the first hop, we have to treat it differently
                if hop == 1:
                    prevHopIPs = [start]
                else:
                    cursor.execute("SELECT distinct ip from traceroute WHERE srcip = ? AND dstip= ? AND hop = ?",(start, dest, hop))
                    prevHopIPs = [ip for (ip,) in cursor.fetchall()]
                for prevHopIP in prevHopIPs:
                # for each hop, find all of the next hops
                    if hop == 1:
                        cursor.execute(get_first_hop_groups, (hop, start, dest))
                    else:
                        cursor.execute(get_groups, (prevHopIP, hop, hop+1, start, dest))
                    if prevHopIP == "*":
                        continue
                    # get the data for all of the subsequent IPs
                    rtts = {}
                    info = {}
                    startEventstamps = {}
                    lengths = {}
                    seenIPs = {}
                    inPrevRun = {}
                    curEventstamp = None
                    totalElems = 0
                    # try to compute the prevalence, persistence, and avg rtt in one pass
                    for (hop, router, eventstamp, ip, rtt) in cursor.fetchall():
                        # if we are at the end of an eventstamp, set
                        # IPs as either in the eventstamp or not
                        if curEventstamp != eventstamp and curEventstamp != None:
                            # go over all of the ips that are currently in the run and see if this is the end of their run
                            for key in inPrevRun.keys():
                                # if this is the end of a run, then mark it as no longer being a run and add the length onto lengths
                                if key not in seenIPs:
                                    if ip in lengths:
                                        lengths[ip].append(curEventstamp-startEventstamps[ip])
                                    else:
                                        lengths[ip] = [curEventstamp-startEventstamps[ip]]
                                    del inPrevRun[ip]
                                    del startEventstamps[ip]
                            # make sure that we mark every element we have seen in this eventstamp as in being in this eventstamp
                            for key in seenIPs.keys():
                                inPrevRun[ip] = True
                                if key not in startEventstamps:
                                    startEventstamps[ip] = curEventstamp
                            seenIPs = {}
                            curEventstamp = eventstamp
                        seenIPs[ip] = True
                        totalElems += 1
                        if ip in rtts:
                            rtts[ip].append(rtt)
                        else:
                            rtts[ip] = [rtt]
                        if ip not in info:
                            info[ip] = {'hop':hop, 'router':router, 'vertex_ip1':prevHopIP, 
                                        'vertex_ip2':ip, 'srcip':start, 'dstip':dest}

                    # for each group, find the avg rtt
                    for ip in rtts.keys():
                        if ip == u'*':
                            continue
                        avgRtt = stats.nanmean(rtts[ip])
                        info[ip]['avg_rtt'] = avgRtt
                        prevalence = float(len(rtts[ip])) / float(totalElems)
                        info[ip]['prevalence'] = prevalence
                        if ip in lengths:
                            persistence = stats.nanmean(lengths[ip])
                        else:
                            persistence = "n/a"
                        info[ip]['persistence'] = persistence
                        outputCursor.execute(insert_data, (info[ip]['router'], info[ip]['srcip'], info[ip]['dstip'], info[ip]['hop'], info[ip]['vertex_ip1'], info[ip]['vertex_ip2'], info[ip]['avg_rtt'], info[ip]['prevalence'], info[ip]['persistence']))
                outputDB.commit()
    outputDB.commit()
    outputDB.close()
    db.close()


def create_table(filename):
    outputDB = sqlite3.connect(filename)
    create_table_query = ("CREATE TABLE monthlyData (deviceid text, srcip text, dstip text, hop integer, vertex_ip1 text, vertex_ip2 text, avg_rtt real, prevalence real, persistence real)")
    outputDB.execute(create_table_query)
    outputDB.commit()
    outputDB.close()

def print_complete(router):
    print "Finished computing prevalence and persistence for router: {}".format(router)
    return

def concurrent_precomputation(filestub, final_output):
    """Compute the monthly data on multiple threads by splitting up the
    computation by each router and then coalescing the result

    Parameters:
    filestub- the common filename for input dbs

    Note: export_data.py must be used to create separate dbs for each
    router before this function may be called

    """
    insert_data = ("INSERT into monthlyData (deviceid, srcip, dstip, hop, vertex_ip1, "
                   "vertex_ip2, avg_rtt, prevalence, persistence) VALUES "
                   "(?, ?, ?, ?, ?, ?, ?, ?, ?)")
    # create a pool of processes to run from
    pool = Pool()

    outputDBs = []
    # find the database files in the current directory
    for filename in os.listdir("."):
        # if this is a database file, then queue it for computation
        if filestub in filename:
            inputDB = filename
            outputDB = filename[:-3] + "-output.db"
            outputDBs.append(outputDB)
            create_table(outputDB)
            pool.apply_async(precompute_monthly_db, [inputDB, outputDB])
    pool.close()
    pool.join()
    # coalesce all of the individual results into 1 db
    outputConn = sqlite3.connect(final_output)
    output = outputConn.cursor()
    numDBs = 0
    for db in outputDBs:
        inputDB = sqlite3.connect(db)
        inputCursor = inputDB.cursor()
        inputCursor.execute("SELECT * from monthlyData")
        for entry in inputCursor.fetchall():
            output.execute(insert_data, entry)
        inputDB.close()
        outputConn.commit()
        numDBs += 1
        print "Coalesced {} dbs".format(numDBs)
    outputConn.close()

if __name__ == "__main__":
    create_table('monthly-data.db')
    # precompute_monthly_db('sqlite-traceroute-data.db', 'monthly-data.db')
    # precompute_monthly_db('one-router.db', 'monthly-data.db')
    concurrent_precomputation('monthly-data-split-','monthly-data.db')
    
