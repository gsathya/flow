#!/usr/bin/env python

import dbhash
import sys
import fnmatch
import cPickle as cp
import sqlite3
import time

def run_insert_query_by_day(conn, key, value, day):
    print "Command Construction"
    for val in value:
        test_time = time.strftime('%Y-%m-%d',time.gmtime(int(key[1])))	
        if test_time != day:
            return
        time_val = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(int(key[1])))	
#        try:
        cmd  = "INSERT into traceroute (deviceid,eventstamp,srcip,dstip,toolid,hop,ip,rtt) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(key[0],time_val,key[2],key[3],key[4],val[0],val[1],val[2]);
            #print cmd
        conn.execute(cmd)
#        except:
#            print "Couldn't run %s\n"%(cmd)
#            continue
    return

def run_insert_query(conn, key, value):
    print "Command Construction"
    for val in value:
        time_val = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(int(key[1])))	
        cmd  = "INSERT into traceroute (deviceid,eventstamp,srcip,dstip,toolid,hop,ip,rtt) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(key[0],time_val,key[2],key[3],key[4],val[0],val[1],val[2]);
        conn.execute(cmd)
    return

def export_day(day, conn):
    db = dbhash.open("traceroutes--2014-01.db", "r")

    for keys in db.keys():
        key = cp.loads(keys)
        value = cp.loads(db[keys])
        retVal = run_insert_query_by_day(conn, key, value, day)
        # if there is an error or we have gone past the correct day,
        # then break out
        # if retVal == False:
        #     break

    conn.commit()
    db.close()

def export_all(conn):
    db = dbhash.open("traceroutes--2014-01.db", "r")
    numAdded = 0

    for keys in db.keys():
        key = cp.loads(keys)
        value = cp.loads(db[keys])
        retVal = run_insert_query(conn, key, value)
        numAdded += 1
        if numAdded > 100:
            conn.commit()
            numAdded = 0

    conn.commit()
    db.close()

def create_table(conn):
    create_table_query = ("CREATE table traceroute (deviceid text, eventstamp text, "
                          "srcip text, dstip text, toolid text, hop integer, ip text, rtt real)")
    conn.execute(create_table_query)
    conn.commit()

def split_data_into_diff_tables(conn, filestub):
    """Split the data into tables of 10 routers each so that we can
    compute the prevalence and persistence in parallel

    """
    get_data = ("SELECT * from traceroute WHERE deviceid = ?")
    get_routers = ("SELECT distinct deviceid from traceroute")
    insert_data = ("INSERT into traceroute (deviceid,eventstamp,srcip,dstip,toolid,hop,ip,rtt) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    cursor = conn.cursor()
    cursor.execute(get_routers)
    fileNum = 0
    dbName = filestub + str(fileNum) + ".db"
    storeDB = sqlite3.connect(dbName)
    create_table(storeDB)
    store = storeDB.cursor()
    routers = cursor.fetchall()
    numUncommitted = 0
    numRouters = 0
    for (router,) in routers:
        cursor.execute(get_data,(router,))
        for entry in cursor.fetchall():
            store.execute(insert_data, entry)
            numUncommitted += 1
            if numUncommitted > 100:
                storeDB.commit()
                numUncommitted = 0
        numRouters += 1
        print "Finished {} routers".format(totRouter)
        storeDB.close()
        fileNum += 1
        dbName = filestub + str(fileNum)
        storeDB = sqlite3.connect(dbName)
        create_table(storeDB)
        store = storeDB.cursor()

if __name__ == "__main__":
    conn = sqlite3.connect('sqlite-traceroute-data.db')
#    create_table(conn)
#    export_day('2014-01-01', conn)
#    export_all(conn)
#    conn.commit()
    split_data_into_diff_tables(conn, "monthly-data-split-")
    conn.close()
