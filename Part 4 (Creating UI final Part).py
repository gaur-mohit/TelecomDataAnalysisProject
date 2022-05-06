# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:45:53 2020

@author: Mohit Gaur
"""
""" Importing liberarys"""
import pandas as pd
import dash
import webbrowser
import dash_html_components as html
import dash_core_components as dc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table as dt
import dash_bootstrap_components as dbc
import re
 
#!pip install dash
app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = None
""" Defining function """
def load_data():
    print("Start of load function")
    data_name = "call_data.csv"
    global call_data
    call_data = pd.read_csv(data_name)
    print(call_data.head())
    data_name = "service_data.csv"
    global service_data
    service_data = pd.read_csv(data_name)
    
    data_name = "device_data.csv"
    global device_data
    device_data = pd.read_csv(data_name)
    
    temp = call_data["Date"].dropna().unique().tolist()
    global start_date_list
    start_date_list = [{"label":str(i),"value":str(i)} for i in temp]
    global end_date_list
    end_date_list = [{"label":str(i),"value":str(i)} for i in temp]
    
    temp = ["Hourly","Daywise","Weekly"]
    
    global  report_type
    report_type=[{"label":str(i),"value":str(i)} for i in temp]
    print("end of load function")

    
def web_browser():
    webbrowser.open_new("http://127.0.0.1:8050")
 
    
 

def creat_app_ui():
    main_layout = html.Div(
        [
        html.H1(children = project_name,id = "Main_title"),
        html.Br(),
        dc.Tabs(id = "Tabs",value="Tab-1",children=[
            dc.Tab(label="Call Data Analysis",id = "Call Data Analysis",value="Tab-1",children=[
                html.Br(),
                html.Br(),
                html.H3(children = "Select Starting Date",id="gg"),
                dc.Dropdown(id = 'Start-time',options = start_date_list, placeholder = "Select Starting Date",value= "2019-06-20" ),
                html.H3(children = "Select Ending Date",id="ff"),
                dc.Dropdown(id = "end-time",options = end_date_list, placeholder = "Select endinging Date",value= "2019-06-25"),
                html.H3(children = "Select Groups",id="kk"),
                dc.Dropdown(id = "Group-DropDown", placeholder="Select Group",multi=True),
                html.H3(children = "Select Report-Type",id="mm"),
                dc.Dropdown(id = "report-type",options = report_type, placeholder = "Select Report Type",value= "Hourly" ),
        
                ]),
            dc.Tab(label="Service Data Analysis",id = "Service Data Analysis",value="Tab-2",children=[
                html.Br(),
                html.H2(children = "Select Date of Service",id = "ddd"),
                dc.Dropdown(id = 'Start-Service-date',options = start_date_list, placeholder = "Select Service  Date",multi = True ),
                
                ]),
            dc.Tab(label="Device Data Analysis",id = "Device Data Analysis",value="Tab-3",children=[
                html.Br(),
                html.H2(children = "Select Date for Device",id = "dgg"),
                dc.Dropdown(id = 'Start-Device-date',options = start_date_list, placeholder = "Select Device Date",multi = True),
                ]),
            
            ]),
        
        
        html.Br(),
        
        dc.Loading( html.Div(id = "Visulations",children='Graph,Card, Table')),
        ]
        )
    
    
    return main_layout


def create_card(title, content, color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.Br(),
                html.Br(),
                html.H2(content, className="card-subtitle"),
                html.Br(),
                ]
        ),
        color=color, inverse=True
    )
    return(card)


def count_devices(data):
    print("start count device function")
    count_de = {"Mac":0,
                 "Polycom":0,
                 "Windows":0,
                 "iphone":0,
                 "Yealink":0,
                 "Aastra":0,
                 "Android" :0,
                 "Others":0}
    re_data = data["UserDeviceType"].dropna().reset_index()
    for i in re_data["UserDeviceType"]:
        if re.search("Polycom",i):
            count_de["Polycom"]+=1
        elif re.search("Mac",i):
            count_de["Mac"]+=1
        elif re.search("Windows",i):
            count_de["Windows"]+=1
        elif re.search("iphone|iOS",i):
            count_de["iphone"]+=1
        elif re.search("Yealink",i):
            count_de["Yealink"]+=1
        elif re.search("Aastra",i):
            count_de["Aastra"]+=1
        elif re.search("Android",i):
            count_de["Android"]+=1
        else:
            count_de["Others"]+=1
    fi_data = pd.DataFrame()
    fi_data["Device"]=count_de.keys()
    fi_data["Count"]=count_de.values()
    print("end count device function")
    return fi_data



@app.callback(
    Output("Visulations","children"),
    [
    Input("Tabs","value"),
    Input("Start-time","value"),
    Input("end-time","value"),
    Input("Group-DropDown","value"),
    Input("report-type","value"),
    Input('Start-Service-date',"value"),
    Input("Start-Device-date","value")
     ]
    )
def update_app_ui(Tabs,start_date,end_date,group_list,report_type,service_date,device_date):
    print("Data Type of start_date value = " , str(type(start_date)))
    print("Data of start_date value = " , str(start_date))
    
    print("Data Type of end_date value = " , str(type(end_date)))
    print("Data of end_date value = " , str(end_date))
    
    
    print("Data Type of group value = " , str(type(group_list)))
    print("Data of group value = " , str(group_list))
    
    print("Data Type of report_type value = " , str(type(report_type)))
    print("Data of report_type value = " , str(report_type))
    
    if Tabs == "Tab-1":
        
        """ ploting graph """
        print("start of update ui")
        call_date_selection = call_data[(call_data['Date']>=start_date) & (call_data['Date']<=end_date)]
        
        if  group_list == [] or group_list is None  :
            pass
        else:
            call_date_selection = call_date_selection[call_date_selection['Group'].isin(group_list)]
            
        graph_data = call_date_selection
        
        if report_type =='Weekly':
            graph_data =  graph_data.groupby("weekly_range")["Call_Direction"].value_counts().reset_index(name= 'Count')
            x= "weekly_range"
            content = call_date_selection["weekly_range"].value_counts().idxmax()
            title = "Busiest Weekday"
             
             
        elif report_type =='Daywise':
            graph_data =  graph_data.groupby("Date")["Call_Direction"].value_counts().reset_index(name= 'Count')
            x= "Date"
            content = call_date_selection[x].value_counts().idxmax()
            title = "Busiest Day"
        else:
            graph_data =  graph_data.groupby("Hourly_range")["Call_Direction"].value_counts().reset_index(name= 'Count')
            x= "Hourly_range"
            content = call_date_selection[x].value_counts().idxmax()
            title = "Busiest Hour"
            
        
        figure = px.area(graph_data,
                          x=x,
                          y="Count",
                          color = 'Call_Direction',
                          hover_data= ["Call_Direction","Count"],
                          template = "simple_white")
        
        figure.update_traces(mode = "lines+markers")
        print("start of update ui")  
        """Card information """
        
        
        total_calls = call_date_selection["Call_Direction"].count()
        card_1 = create_card("Total Calls",total_calls, "success")
          
        incoming_calls = call_date_selection["Call_Direction"][call_date_selection["Call_Direction"]=="Incoming"].count()
        card_2 = create_card("Incoming Calls", incoming_calls, "primary")
          
        outgoing_calls = call_date_selection["Call_Direction"][call_date_selection["Call_Direction"]=="Outgoing"].count()
        card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")
          
        missed_calls = call_date_selection["Missed_Call"][call_date_selection["Missed_Call"] == 19].count()
        card_4 = create_card("Missed Calls", missed_calls, "danger")
          
        max_duration = call_date_selection["Duration"].max()
        card_5 = create_card("Max Duration", f'{max_duration} min', "dark")
        
        card_6 = create_card(title, content, "primary")
             
        graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card_1], md=3), dbc.Col(id='card2', children=[card_2], md=3)])
        graphRow1 = dbc.Row([dbc.Col(id='card3', children=[card_3], md=3), dbc.Col(id='card4', children=[card_4], md=3)])
        graphRow2 = dbc.Row([dbc.Col(id='card5', children=[card_5], md=3), dbc.Col(id='card6', children=[card_6], md=3)])
     
        cardDiv = html.Div([graphRow0,html.Br(),graphRow1,html.Br(), graphRow2])
        
    
        
        
        
        """table"""
        datatable_data = call_date_selection.groupby(["Group","UserID","UserDeviceType"])["Call_Direction"].value_counts().unstack(fill_value=0).reset_index()
        if call_date_selection["Missed_Call"][call_date_selection["Missed_Call"]==19].count()!=0:
            datatable_data["Missed_Call"] = call_date_selection.groupby(["Group","UserID","UserDeviceType"])["Missed_Call"].value_counts().unstack()[19]
        else:
            datatable_data["Missed_Call"] =0
        datatable_data["Total_Call_duration"]=call_date_selection.groupby(["Group","UserID","UserDeviceType"])["Duration"].sum().tolist()
        
        datatable = dt.DataTable(
            id='table',
            columns = [{"name":i,"id":i} for i in datatable_data.columns],
            data = datatable_data.to_dict('records'),
            page_current = 0,
            page_size = 20,
            page_action = 'native',
            style_header={'backgroundColor':'rgb(30,30,30)'},
            style_cell = {'backgroundColor':'rgb(50,50,50)',
                          'color':'white'
                          
                })
           
        print("end of update ui")
        return [
            dc.Graph(figure=figure),
                html.Br(),
                cardDiv,
                html.Br(),
                datatable
                ]
    elif Tabs == "Tab-3":
        print("start device data")
       
        if device_date is None or device_date ==[]:
            device_a = count_devices(device_data)
        else:
            z = device_data[device_data["DiviceEventDate"].isin(device_date)]
            device_a = count_devices(z)
        fig= px.pie(device_a,names= "Device",values="Count",color = "Device",hole = .3)
        fig.update_layout(autosize=True,
                          margin = dict(l=0,r=0,t=25,b=20),
                          )
        print("end device data")
        return dc.Graph(figure = fig)
    
    elif Tabs == "Tab-2":
        if service_date is None or service_date ==[]:
            service_a = service_data["Featurename"].value_counts().reset_index(name = "Count")
        else:
            service_a = service_data["Featurename"][service_data["FeatureEventDate"].isin(service_date)].value_counts().reset_index(name="Count")
        
        fig= px.pie(service_a,names= "index",values="Count",color = "index")
        fig.update_layout(autosize=True,
                          margin = dict(l=0,r=0,t=25,b=20),
                          )
        print("end Service data")
        return dc.Graph(figure = fig)   
    else:
        return None
        








@app.callback(
    Output("Group-DropDown","options"),
    [
    Input("Start-time","value"),
    Input("end-time","value")
    ]
    )
def update_group(start_date,end_date):
    reformed_data = call_data[(call_data["Date"]>=start_date)&(call_data["Date"]<=end_date)]
    group_list = reformed_data['Group'].unique().tolist()
    group_list = [{"label":m,"value":m} for m in group_list]
    
    return group_list
    



def main ():
    print("satrt of Main function")
    
    load_data()
    web_browser()
    global project_name
    project_name = "CDR Data Analysis Project"
    
    global app
    app.layout = creat_app_ui()
    app.title = project_name
    app.run_server()
    
    
    print("end of main function")
    app = None
    project_name = None
    global call_data,service_data,start_date_list,end_date_list,report_type,device_data
    
    service_data=None
    call_data=None
    device_data=None
    start_date_list=None
    end_date_list=None
    report_type=None
    
if (__name__=="__main__"):
   
    main()
    
