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

if __name__ == "__main__":
    conn = sqlite3.connect('sqlite-traceroute-data.db')
#    create_table(conn)
#    export_day('2014-01-01', conn)
    export_all(conn)
    conn.commit()
    conn.close()
