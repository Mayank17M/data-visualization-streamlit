import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

uber_path = "datasets/uber-raw-data-apr14.csv"
ny_path = "datasets/ny-trips-data.csv"
netflix = "datasets/netflix_titles.csv"

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

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