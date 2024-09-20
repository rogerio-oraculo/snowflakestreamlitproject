import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
import json

st.title("Análisis de Stop and Search en Londres")

# Conectar con Snowflake
def get_snowflake_connection():
    with open('connection.json') as f:
        connection_parameters = json.load(f)
    return snowflake.connector.connect(**connection_parameters)

@st.cache_data(ttl=600)
def load_stop_and_search_data():
    conn = get_snowflake_connection()
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_stop_and_search" LIMIT 100;"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cargar los datos
stop_search_data = load_stop_and_search_data()

# Mostrar datos
st.dataframe(stop_search_data)

# Gráfico
fig = px.histogram(stop_search_data, x="GENDER", color="OUTCOME", barmode="group")
st.plotly_chart(fig)
