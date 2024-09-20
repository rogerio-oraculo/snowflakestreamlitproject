import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
import json

st.title("Análisis de Crímenes Callejeros en Londres")

# Conectar con Snowflake
def get_snowflake_connection():
    with open('connection.json') as f:
        connection_parameters = json.load(f)
    return snowflake.connector.connect(**connection_parameters)

@st.cache_data(ttl=600)
def load_street_data():
    conn = get_snowflake_connection()
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_street" LIMIT 100;"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cargar los datos
street_data = load_street_data()

# Mostrar datos
st.dataframe(street_data)

# Gráfico
fig = px.scatter_mapbox(street_data, lat="LATITUDE", lon="LONGITUDE", color="CRIME_TYPE", zoom=10)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)
