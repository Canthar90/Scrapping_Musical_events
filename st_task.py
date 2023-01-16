import streamlit as st
import plotly.express as px
import sqlite3


connection = sqlite3.connect("data.db")
cursor =  connection.cursor()
st.title("Temperature plot")

cursor.execute("SELECT * FROM temperatures")
new_list = cursor.fetchall()



x = [elem[0] for elem in new_list[1:]]
y = [elem[1] for elem in new_list[1:]]


figure = px.line(x=x, y=y, labels={"x": "Date", "y": "Temperature"})

st.plotly_chart(figure)