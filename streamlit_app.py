import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

uber_path = "datasets/uber-raw-data-apr14.csv"
ny_path = "datasets/ny-trips-data.csv"
netflix = "datasets/netflix_titles.csv"

def myDecorator(function):
    def modified_function(df):
        time_ = time.time()
        res = function(df)
        time_ = time.time()-time_
       # with open(f"{function.__name__}_exec_time.txt","w") as f:
       #     f.write(f"{time_}")
        return res
    return modified_function


@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

@myDecorator
@st.cache
def df1_data_transformation(df_):
    df = df_.copy()
    df["Date/Time"] = df["Date/Time"].map(pd.to_datetime)

    def get_dom(dt):
        return dt.day
    def get_weekday(dt):
        return dt.weekday()
    def get_hours(dt):
        return dt.hour

    df["weekday"] = df["Date/Time"].map(get_weekday)
    df["dom"] = df["Date/Time"].map(get_dom)
    df["hours"] = df["Date/Time"].map(get_hours)

    return df

@myDecorator
@st.cache
def df2_data_transformation(df_):
    df = df_.copy()
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    def get_hours(dt):
        return dt.hour

    df["hours_pickup"] = df["tpep_pickup_datetime"].map(get_hours)
    df["hours_dropoff"] = df["tpep_dropoff_datetime"].map(get_hours)

    return df

@st.cache(allow_output_mutation=True)
def frequency_by_dom(df):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_title("Frequency by DoM - Uber - April 2014")
    ax.set_xlabel("Date of the month")
    ax.set_ylabel("Frequency")
    ax = plt.hist(x=df.dom, bins=30, rwidth=0.8, range=(0.5,30.5))
    return fig

@st.cache
def map_data(df):
    df_ = df[["Lat","Lon"]]
    df_.columns=["lat","lon"]
    return df_

def Uber_dataset():
    #Uber-raw-data-apr14 dataset
    st.title("Uber data visualization")

    ## Load the Data
    st.text(" ")
    st.header("Load the Data")
    st.text(" ")
    df1 = load_data(uber_path)
    if st.checkbox('Show dataframe'):
        df1

def Ny_dataset():
    #ny-trips-data dataset
    st.title("New York taxi trips")

    ## Load the Data
    st.text(" ")
    st.header("Load the Data")
    st.text(" ")
    df2 = load_data(ny_path)
    if st.checkbox('Show dataframe 2'):
        df2

def netflix_data():
    #Netflix dataset
    st.title("Netflix Movies and TV shows")

    ## Load the Data
    st.text(" ")
    st.header("Load the Data")
    st.text(" ")
    df3 = load_data(netflix)
    if st.checkbox('Show dataframe'):
        df3


def main():

    choice = st.sidebar.selectbox(
    'Choose your dataset',
    ('Uber NYC dataset', 'NYC taxi trip dataset', 'Netflix dataset'))

    if choice == 'Uber NYC dataset':
        Uber_dataset()
    elif choice == 'NYC taxi trip dataset':
        Ny_dataset()
    else:
        netflix_data()

main()