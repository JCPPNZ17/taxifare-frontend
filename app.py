import datetime  # build the pickup datetime from date + time widgets

import requests  # call the local FastAPI backend
import streamlit as st  # the frontend framework

st.title("TaxiFare 🚕")  # page title

api_url = st.secrets["API_URL"]

pickup_date = st.date_input("Pickup date", datetime.date(2014, 7, 6))  # date part of the ride
pickup_time = st.time_input("Pickup time", datetime.time(19, 18))  # time part of the ride
pickup_longitude = st.number_input("Pickup longitude", value=-73.950655, format="%.6f")  # %.6f keeps GPS precision
pickup_latitude = st.number_input("Pickup latitude", value=40.783282, format="%.6f")
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.984365, format="%.6f")
dropoff_latitude = st.number_input("Dropoff latitude", value=40.769802, format="%.6f")
passenger_count = st.number_input("Passengers", min_value=1, max_value=8, value=1, step=1)  # int input

if st.button("Predict fare"):  # only call the API on click, not on every rerun
    params = {
        "pickup_datetime": f"{pickup_date} {pickup_time}",  
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": int(passenger_count),  # cast to int so the API gets 1, not 1.0
    }
    response = requests.get(api_url, params=params)  # requests builds the query string from params
    if response.status_code == 200: 
        fare = response.json()["fare"]  # key must match what fast.py returns
        st.success(f"Estimated fare: ${fare:.2f}") 
    else:
        st.error(f"API error {response.status_code}: {response.text}")  