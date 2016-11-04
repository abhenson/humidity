#! /usr/bin/python3
"""runs c program that gets temperature and humidity data from the rht03 sensor and
 saves it to an html file that can be used by node.js and to an sqlite3 db"""

from subprocess import Popen, PIPE
import time
from numpy import mean
import sqlite3


def readValue():
    """runs c programs then extracts the readings and formats them
    returns temperature float and humid float
    """
    reader = Popen(["sudo", "/home/abhpi/rht03/rht03"],\
                   stdout=PIPE, stderr=PIPE)
    reading = reader.stdout.readline()
    reading = reading.decode('utf-8')
    #print(reading)
    split_on_temp = reading.split('Temp: ')[1].split()
    temp = split_on_temp[0][:-1]  # :-1 to get rid of excess comma
    humid = split_on_temp[2][:-1]  # getting rid of %
    return temp, humid

def loop(repeats):
    """tries for a 'max_tries' to get data that is above the 'threshold'if it finds
    5 good sets it moves on but if it exceeds the 'max_tries' it will raise an exception
    returns: the rounded average of temp and of humidity"""
    threshold = 1
    max_tries = 60
    temps = []
    humids = []
    tries = 0
    while True:
        tries += 1
        if tries >= max_tries:
            raise Exception
        temp, humid = readValue()
        time.sleep(0.1)
        temp = float(temp)
        humid = float(humid)
        if not temp < threshold and not humid < threshold:
            temps.append(temp)
            humids.append(humid)
        if len(temps) >= 5:
            break
    return round(mean(temps), 1), round(mean(humids), 1)
	

def save2file(temp, humid):
    """takes 'temp' float and 'humid' float and saves to an html file"""
    now = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    with open('/home/abhpi/rht03/current.html','w') as fout:
        fout.write("<h1>Time:{}, <font color='#E44424'>Temp:{}</font>,\
                     <font color='#67BCB'>Humidity:{}</font></h1>".\
                     format(now, temp, humid))


def save2db(temp, humid):
    """takes 'temp' fleat and 'humid'float and saves to sqlite3 db"""
    conn = sqlite3.connect("/home/abhpi/rht03/db.sqlite3")
    c = conn.cursor()
    now = time.time()
    c.execute("INSERT INTO Measurements VALUES ({}, {}, {})".format(now, temp, humid))
    conn.commit()
    conn.close() 


def main():
    repeats = 5
    try:
        temp, humid = loop(repeats=repeats)
    except Exception:
        temp, humid = 0, 0
    save2file(temp, humid)
    save2db(temp, humid)

if __name__ == "__main__":
    main()
