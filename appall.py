# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 21:13:48 2023

@author: karthik
"""

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pickle
import numpy
import pandas
import gunicorn

class model(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

pickle_in = open('clsfrxg.pkl','rb')#xgboost
cls1 = pickle.load(pickle_in)

pickle_in2 = open('clsfr.pkl','rb')#random forest
cls2  = pickle.load(pickle_in2)

pickle_in3 = open('clsfrlo.pkl','rb')#logistic Regression
cls3 = pickle.load(pickle_in3)

def predic(df, num :int):
    if(num==1):
        return cls1.predict(df)
    elif(num==2):
        return cls2.predict(df)
    else:
        return cls3.predict(df)

myApp = FastAPI()

@myApp.get("/")
def homeFunction():
    return "Hello"

@myApp.post("/water_quality")
def getStudent(quer : model, mdl : int):
    query = quer.dict()
    parameters = [[query['ph'],query['Hardness'],query['Solids'],query['Chloramines'],query['Sulfate'],query['Conductivity'],query['Organic_carbon'],query['Trihalomethanes'],query['Turbidity']]]
    arr = numpy.array(parameters, dtype=float)
    columns = []
    for i in query.keys():
        columns.append(i)
    df = pandas.DataFrame(arr, columns=columns)
    output = predic(df, mdl)
    if(output[0]==1):
        return "Safe to drink"
    else:
        return "Unsafe to drink"

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker mai:myApp
async io.run(myApp)