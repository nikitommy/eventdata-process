#!/usr/bin/env python
import rosbag
from tqdm import tqdm
import pandas as pd
import os
import numpy as np

def basename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    return a

def reader(filesname):
    #Read events in filesname.bag
    bag=rosbag.Bag(filesname)
    with open("./GoPro/{}.txt".format(basename(filesname)),'w') as f: 
        for i,(topic,msgs,t) in enumerate(bag.read_messages(topics=['/cam0/events'])):
            for single_event in tqdm(msgs.events):  
                f.write(str(single_event.ts.secs+single_event.ts.nsecs*1.0/1000000000)+' ')         
                f.write(str(single_event.x)+' ')
                f.write(str(single_event.y)+' ')
                if(single_event.polarity==True):        
                    f.write("1")
                else:
                    f.write("-1")
                f.write('\n')  
            print("Writing events between two pic, now is "+ str(i)+'!')
    print("Writing is over!")
    bag.close()

def event2array(eventfilename):
    #Read events and convert events to dict
    event = pd.read_csv(eventfilename, names=['t','x','y','p'], header=None, sep=' ')
    
    t = np.array(list(event['t']))
    t = np.trunc(t * 1e9).astype(int)
    x = np.array(list(event['x'])).astype(int)
    y = np.array(list(event['y'])).astype(int)
    p = np.array(list(event['p'])).astype(int)
    
    event = {'x': x, 'y': y, 'p': p, 't': t}
    return event

def filter_events(event_data, start, end):
    ## filter events based on temporal dimension
    x = event_data['x'][event_data['t']>=start]
    y = event_data['y'][event_data['t']>=start]
    p = event_data['p'][event_data['t']>=start]
    t = event_data['t'][event_data['t']>=start]
    
    x = x[t<=end]
    y = y[t<=end]
    p = p[t<=end]
    t = t[t<=end]

    event = {'x': x, 'y': y, 'p': p, 't': t}
    return event

def custombasename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    a = np.array(a)  
    a = (a.astype(float)*1e7).astype(int)
    return a

