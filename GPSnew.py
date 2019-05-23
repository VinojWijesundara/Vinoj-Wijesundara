#!/usr/bin/env python
# this code for GPS module (NEO-6M), to get cordinates and speed 
import os
import serial
import sys
import time
import datetime


def readString():
    while 1:
        while ser.read().decode("utf-8") != '$': # wait for the string and decode
            pass      # 
        line = ser.readline().decode("utf-8")   # read string
        return line
 
        
def getTime(string,format,returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format))


def getLatLng(latString,lngString):
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")#LATITUDE
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")#Longitude
    lat = 0
    lng = 0
    return lat,lng

def printRMC(lines):
    #global counter
    print("------------RMC=Global=counter----------------")
    print(datetime.datetime.utcnow()) #print date n time in UTC, U can use any format
    latlng = getLatLng(lines[3],lines[5]) 
    print("Lat,Long: ", latlng[0], lines[4], ", ", latlng[1], lines[6], sep='')
    print("Speed (knots):", lines[7])
    print("Status (A=OK,V=NO):", lines[2])
    if len(lines) == 13: # it will return 13 
        print(lines[11])
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[12].partition("*")[0])
    else:
        print(lines[11].partition("*")[0])
    
    return
    


def printVTG(lines):
    print("--------------------Ground speed---------------")
    print("Ground speed (km/h):", lines[7], lines[8].partition("*")[0])#print speed in km per hour
     
    return

def checksum(line):
    checkString = line.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)
        
    try: 
        inputChecksum = int(checkString[2].rstrip(), 16);
    except:
        print("Error in string")
        return False
    
    if checksum == inputChecksum:
        return True
    else:
        print("============================CHECKSOME ERROR!==================================")
        
        print(hex(checksum), "!=", hex(inputChecksum))
        return False
    
if __name__=='__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1) #Open serial port
    try:
        while 1:
            line = readString()
            lines = line.split(",")
            if checksum(line):
                if lines[0] == "GPRMC" :
                    printRMC(lines)     
                    pass
                elif lines[0] == "GPVTG":
                    printVTG(lines)  
                    pass
                
    except KeyboardInterrupt:
        print('Exiting Script')
        


