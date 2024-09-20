import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.title("Análisis de Crímenes Callejeros en Londres")

# Conectar com Snowflake usando o secrets.toml
def get_snowflake_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        role=st.secrets["snowflake"]["role"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

@st.cache_data(ttl=600)
def load_street_data():
    conn = get_snowflake_connection()
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_street" LIMIT 100;"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados
street_data = load_street_data()

# Mostrar os dados em um dataframe interativo
st.dataframe(street_data)

# Gráfico
fig = px.scatter_mapbox(street_data, lat="LATITUDE", lon="LONGITUDE", color="CRIME_TYPE", zoom=10)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)
