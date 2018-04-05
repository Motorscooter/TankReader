# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:33:30 2018

@author: scott.downard
"""

import os
from scipy.signal import filtfilt
import struct
import numpy as np


def fileRead(directory):
    inflatorData = {}

    for file in directory:
        filedict = {}
        new_float_data = []
        new_data = []
        time = []
# =============================================================================
# Opens current file and reads text data to pull needed information
        with open(file,'rb') as fup:
        
            textfilestr = fup.read()
            textfilestr = textfilestr.decode('latin-1') #Decode text from binary file
            vs = textfilestr.find('VERTSCALE')     #Vertical scaling factor
            vo = textfilestr.find('VERTOFFSET')    #Vertical offset from 0
            vu = textfilestr.find('VERTUNITS')     #Vertical units
            hs = textfilestr.find('HORZSCALE')     #horizontal scaling factor
            ho = textfilestr.find('HORZOFFSET')    #horizontal offset from 0
            hu = textfilestr.find('HORZUNITS')     #horizontal units
            hups = textfilestr.find('HUNITPERSEC') #number of horizontal units per second
            rl = textfilestr.find('RECLEN')        #Number of datapoints in file
            xdc = textfilestr.find('XDCRSENS')     #Used to find grab the correct number of points in datapoint line
            cr = textfilestr.find('DDR_RATE')    #Sample rate
            ss = textfilestr.find('EXTMASTER')  #Used to grab correct number of points in Sample Rate
#            name_start = textfilestr.find('Sample')#Reads BuildSheet Number
#            name_end = textfilestr.find('InflatorID')
#            name = str(textfilestr[name_start+6:name_end-1])
            filename , file_extension = os.path.splitext(file)
            namelist = filename.split("/")
            name = namelist[-1]
            filedict[name] = {}
            
            filedict[name]['VertScale'] = float(textfilestr[vs+10:vo - 1])
            filedict[name]['VertOffset'] = float(textfilestr[vo+11:vu - 1])
            filedict[name]['VertUnits'] = textfilestr[vu+10:hs - 1]
            filedict[name]['HorzScale'] = float(textfilestr[hs+10:hups - 1])
            filedict[name]['HorzUnitsPerSec'] = float(textfilestr[hups+12:ho - 1])
            filedict[name]['HorzOffset'] = float(textfilestr[ho+11:hu - 1])
            filedict[name]['HorzUnits'] = (textfilestr[hu+10:rl - 1])
            filedict[name]['NumofPoints'] = int(textfilestr[rl+7:xdc-1])
            filedict[name]['Sample Rate'] = float(textfilestr[cr+9:ss-1])
            filedict[name]['Color'] = '#000000'
        fup.close()            
# =============================================================================
# =============================================================================
# The file is closed and then opened to read binary data.
        with open(file, 'rb') as fup:
            datacount = filedict[name]['NumofPoints']
            filedict[name]['RawYData'] = []            
            size = fup.read()
            data = struct.unpack('h'*datacount,size[len(size)-(datacount*2):])
            list_data = list(data)
            for i in list_data:
                new_float_data.append(float(i))
            for i in new_float_data:
                new_data.append(i *  filedict[name]['VertScale'] + filedict[name]['VertOffset'])
            filedict[name]['RawYData'] = new_data
            timecount = filedict[name]['HorzOffset']           
            for i in range(0,filedict[name]['NumofPoints']):
                time.append(timecount)
                timecount += filedict[name]['HorzScale']
            filedict[name]['XData'] = time
        fup.close()
        inflatorData.update(filedict)
# =============================================================================    
    return inflatorData

# =============================================================================
# Filter Data using SAE filter standards
def filterProcessing(data_frame,CFC,sample_rate):    
    #calculate sample rate
    #Filter RAW data using J211 SAE Filtering
    sample_rate = int(sample_rate)
    T = 1/sample_rate
    wd = 2 * np.pi * CFC * 1.25*5.0/3.0
    x = wd * (T)/2
    wa = np.sin(x)/np.cos(x)
    
    a0 = wa**2.0/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    a1 = 2.0*a0
    a2 = a0
    b0 = 1
    b1 = (-2.0*((wa**2.0)-1.0))/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    b2 = (-1.0+np.sqrt(2.0)*wa-(wa**2.0))/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    b  = [a0,a1,a2]
    a = [b0,-1*b1,-1*b2]
#    CFC = 5/3*CFC
#    wn = CFC/sample_rate * 2
#    b,a = butter(2,wn,'low')
    y = filtfilt(b,a,data_frame)
    return y
# =============================================================================
#Taken out because of issues calculating TTFG
#def ttfgCalc(rawpressure,time):
## =============================================================================
## Calculate TTFG (Time to First Gas)
##    neglist = []
##
##    for i in rawpressure:
##        if i < 0:
##            neglist.append(i)
##    index = neglist.index(neglist[-1])
##    index += 250
##    ttfg = time[index]
#    start = 0
#    end = 100
#    slope = 0
#    while slope < 1.00:
#
#        y1 = rawpressure[start]
#        y2 = rawpressure[end]
#        x1 = time[start]
#        x2 = time[end]
#        slope = (y2-y1)/(x2-x1)
#        if slope > 0.75:
#            break
#        start += 100
#        end += 100
#    ttfg = time[start]
#    return ttfg   
# =============================================================================
# =============================================================================
# Calculate Pmax Maximum pressure
def pMax(pressure):
    Pmax = max(pressure)  
    return Pmax
# =============================================================================
# =============================================================================
# Calculate rise rate (Gtx) @ 20-40%
def gtx(pressure,time):
    pressure = pressure.tolist()
    pmax = max(pressure)
        #find 20% of max pressure
    p20 = pmax * 0.20
#    find 40% of max pressure
    p40 = pmax * 0.40
    y2 = min(pressure, key = lambda x:abs(x-p40))
    y1 = min(pressure, key = lambda x:abs(x-p20))
    index2 = pressure.index(y2)
    index1 = pressure.index(y1)
    x2 = time[index2]
    x1 = time[index1]
    gtx24 = (y2-y1)/(x2 - x1) 
   
    return gtx24
# =============================================================================    
# =============================================================================
# Calculate the start of the event which is the time at 10% of pressure
def eventStart(pressure,time):
    pressure = pressure.tolist()
    pmax = max(pressure)
    p10 = pmax * 0.10
    p10 = min(pressure, key = lambda x:abs(x-p10))
    index = pressure.index(p10)
    start = time[index]
    return start 
# =============================================================================
