# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:09:15 2020

@author: Sona Gaur
"""
# All imports 
import pandas as pd
import re
import numpy as np
import datetime


""" functions"""

def datetime_divider(x):
    for i in range(len(x)):
        if re.match("^\d",str(x[i])):
            regex=re.compile("\d{1,8}")
            a = regex.findall(str(x[i]))
            x[i]=[a[0],a[1]]
        else:
            x[i]=[np.nan,np.nan]
    return x

def date_modifer(x):
    for i in range(len(x)):
        if re.match("^\d",str(x[i])):
            year = str(x[i][:4])
            month= str(x[i][4:6])
            day = str(x[i][6:])
            x[i]='-'.join([year,month,day])
        else:
            x[i]=np.nan
    return x

def time_modifer(x):
    for i in range(len(x)):
        if re.match("^\d",str(x[i])):
            hour = int(x[i][:2])
            mi = (x[i][2:4])
            sec=(x[i][4:])
            if (hour) >=12:
                if hour==12:
                    hr = str(hour)
                else:
                    hr = str(hour-12)
                du = "PM"
            else:
                du = "AM"
                if hour == 0:
                    hr=str(12)
                else:
                    hr = x[i][:2]
            x[i]=":".join([hr,mi,sec])+" "+du
        else:
             x[i] = np.nan
    return x
            
def replace_sample_with_std_termonology(x):
    x[5] = x[5].replace("Originating","Outgoing")
    x[5] = x[5].replace("Terminating","Incoming")
    x[267] = x[267].replace("Success","Voice Portal")
    x[312] = x[312].replace("Shared Call Appearance","Secondary Device")
    return x

def call_time_modifier(x):
    for i in range(len(x)):
        x[i]=str(x[i])
        if x[i]!="nan":
            y= x[i][:4]
            mo=x[i][4:6]
            da=x[i][6:8]
            h= x[i][8:10]
            mi=x[i][10:12]
            se = str(round(float(x[i][12:])))
            if int(se)>=60:
                se = int(se)-60
                mi =int(mi)+1
            if int(mi)>=60:
                
                mi =int(mi)-60
                h =int(h)+1            
            x[i] = f"{y}-{mo}-{da} {h}:{mi}:{se}"
        else:
            x[i] = np.nan
    return x

def hourly_range(x):
    for i in range(len(x)):
        x[i]=str(x[i])
        if x[i]!="nan":
            if re.search("PM",x[i]):
                time_data = re.findall("\d+",x[i])
                if time_data[0]!="12":
                    time_data=int(time_data[0])+12
                else:
                    time_data =time_data[0]
            else:
                 time_data = re.findall("\d+",x[i])
                 if int(time_data[0])==12:
                     time_data = f"0{int(time_data[0])-12}"
                 else:
                      time_data =time_data[0]
            x[i] = f"{time_data}:00 - {time_data}:59"
        else:
             x[i]=np.nan
    return x

def weekly_range(x):
    for i in range(len(x)):
        x[i]=str(x[i])
        if x[i]!="nan":
            y,m,d=[int(j) for j in x[i].split("-")]
            ans= datetime.date(y,m,d)
            x[i]=ans.strftime("%A")
        else:
            x[i] = np.nan
    return x

def combine_all_service(x,y,z):
    for i in range(len(x)):
        if x[i] is np.nan:
            if y[i] is not np.nan and z[i] is not np.nan:
                x[i]=str(y[i])+" "+str(z[i])
            elif y[i] is not np.nan : 
                x[i]=y[i]
            else:
                x[i]=z[i]
        else:
            continue
    return x

def remove_unwanted_data(x):
    for i in range(len(x)):
        if x[i]=="Secondary Device" or x[i]=="Primary Device":
            continue
        else:
            x[i] = np.nan
    return x
        
    
                
                                           
    
    
                
    
"""Main Program"""
# reading data into data
data=pd.read_csv("raw_cdr_data.csv",header=None,low_memory=False)
print(data.head(10))
print(data.shape)
print(data[9].value_counts())
print(data[9].isnull().value_counts())
print(data[data[9].isnull()])
print(data[9].head(50))


# changing the formate of coloum 9
data["Date"],data["Time"]=zip(*datetime_divider(data[9].tolist()))
print(data["Date"].head(20),data["Time"].head(20))
data["Date"]=date_modifer(data["Date"])
print(data["Date"].head(20))
data["Time"] = time_modifer(data["Time"]) 
print(data["Time"].head(20))
data = replace_sample_with_std_termonology(data)
print(data[5].unique())
print(data[267].unique())
print(data[312].unique())

data[312]= remove_unwanted_data(data[312])
print(data[312].unique())
print(data[9].head(20))
data["starttime"]=pd.to_datetime(call_time_modifier(data[9].tolist()))
print(data["starttime"].head(20))

data["endtime"] = pd.to_datetime(call_time_modifier(data[13].tolist()))
print(data["endtime"].head(20))

data["Duration"]=(data["endtime"]-data["starttime"]).astype("timedelta64[m]")
print(data["Duration"].sample(20))

data["weekly_range"]= weekly_range(data["Date"].tolist())
print(data["weekly_range"].head(20))

data["Hourly_range"]=hourly_range(data["Time"].tolist())
print(data["Hourly_range"].head(20))

data[147]=combine_all_service(data[147].tolist(),data[312].tolist(),data[267].tolist())
print(data[147].head(50))

data = data.drop("Time",axis = 1)
data.to_csv("Cdr_data.csv",index = None)