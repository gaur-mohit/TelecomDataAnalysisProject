# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:52:18 2020

@author: Mohit Gaur
"""

""" Importing liberarys"""
import pandas as pd


""" Defining function """
def main ():
    
    data_name = "cdr_data.csv"
    call_data_coloums= ["4","5","14","31","120","147","267","312","345","Date","starttime","endtime",\
                        "Duration","Hourly_range","weekly_range"]
        
    call_data = pd.read_csv(data_name,usecols=call_data_coloums,low_memory = False)
    
    service_data_coloums =["31","120","147","345","Date","starttime","endtime","Duration"]
    
    service_data = pd.read_csv(data_name,usecols=service_data_coloums ,low_memory = False)
    
    device_data_coloums = ["5","31","120","312","345","Date","starttime","endtime","Duration"]
    
    device_data = pd.read_csv(data_name,usecols=device_data_coloums ,low_memory = False)
    
    
    call_data = call_data.rename(columns={"4":"Group","5":"Call_Direction","14":"Missed_Call",
                                  "31":"GroupID","120":"UserID","147":"Features","267":"VPDialingFacResult",
                                  "312":"UsageDeviceType",
                                  "345":"UserDeviceType"})
    
    service_data = service_data.rename(columns={"31":"GroupId","120":"UserID","147":"Featurename",
                                        "345":"UserDeviceType","Date":"FeatureEventDate"})
    
    device_data = device_data.rename(columns={"31":"GroupId","120":"UserID","5":"DeviceEventTypeDirection",
                                        "345":"UserDeviceType","Date":"DiviceEventDate","312":"UsegeDeviceType"})
    print(device_data["UserDeviceType"].head(20))
    print(call_data.head(20))
    print(service_data.head(20))
    print(device_data.head(20))
    call_data.to_csv("Call_data.csv",index=None)
    service_data.to_csv("service_data.csv",index=None)
    device_data.to_csv("device_data.csv",index=None)
    

if (__name__=="__main__"):
    main()
    
    
    
    
