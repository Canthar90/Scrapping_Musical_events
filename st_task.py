import streamlit as st
import plotly.express as px


st.title("Temperature plot")

with open("temperatures.txt", "r") as file:
    content_list = file.readlines()


new_list = [(elem.strip().split(',')) for elem in content_list]
x = [elem[0] for elem in new_list[1:]]
y = [elem[1] for elem in new_list[1:]]


figure = px.line(x=x, y=y, labels={"x": "Date", "y": "Temperature"})

st.plotly_chart(figure)