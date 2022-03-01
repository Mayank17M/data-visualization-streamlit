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

@st.cache(allow_output_mutation=True)
def data_by(by,df):
    def count_rows(rows):
        return len(rows)
    
    if by == "dom":
        fig, ax = plt.subplots(1,2, figsize=(10,6))
        ax[0].set_ylim(40.72,40.75)
        ax[0].bar(x=sorted(set(df["dom"])),height=df[["dom","Lat"]].groupby("dom").mean().values.flatten())
        ax[0].set_title("Average latitude by day of the month")

        ax[1].set_ylim(-73.96,-73.98)
        ax[1].bar(x=sorted(set(df["dom"])),height=df[["dom","Lon"]].groupby("dom").mean().values.flatten(), color="orange")
        ax[1].set_title("Average longitude by day of the month")
        return fig
    
    elif by == "hours":
        fig, ax= plt.subplots(figsize=(10,6))
        ax = plt.hist(x=df.hours, bins=24, range=(0.5,24))
        return fig
    
    elif by == "dow":
        fig, ax= plt.subplots(figsize=(10,6))
        ax = plt.hist(x=df.weekday, bins=7, range=(-5,6.5))
        return fig
    
    elif by == "dow_xticks":
        fig, ax= plt.subplots(figsize=(10,6))
        ax.set_xticklabels('Mon Tue Wed Thu Fri Sat Sun'.split())
        ax.set_xticks(np.arange(7))
        ax = plt.hist(x=df.weekday, bins=7, range=(0,6))
        return fig
    
    else:
        pass

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

    ## Perform Data Transformation
    df1_ = df1_data_transformation(df1)

    ## Visual representation
    st.text(" ")
    st.text(" ")
    st.header("Visual representation")
    if st.checkbox("Show graphs"):
        st.text(" ")
        st.markdown("`Frequency by day of the month`")
        st.pyplot(frequency_by_dom(df1_))

        #
        st.text(" ")
        st.markdown("`Viewing points on a map`")
        st.map(map_data(df1_))

        #
        st.text(" ")
        st.markdown("`Visualization of data per hour`")
        st.pyplot(data_by("hours",df1_))

        #
        st.text(" ")
        st.markdown("`Visualization of data by day of the week`")
        st.pyplot(data_by("dow",df1_))

        #
        st.text(" ")
        st.markdown("`Visualization of data by day of the week with the names of the days in abscissa`")
        st.pyplot(data_by("dow_xticks",df1_))

        #
        st.text(" ")
        st.markdown("`Mean latitude and longitude by day of the month`")
        plt.gcf().subplots_adjust(wspace = 0.3, hspace = 0.5)
        st.pyplot(data_by("dom",df1_))

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

    ## Perform Data Transformation
    st.text(" ")
    df2_ = df2_data_transformation(df2)

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