import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.title("Stop and Search Analysis in London")

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
def load_stop_and_search_data():
    conn = get_snowflake_connection()
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_stop_and_search";"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados
stop_search_data = load_stop_and_search_data()

# Filtros na barra lateral
genders = st.sidebar.multiselect("Select Gender", options=stop_search_data["GENDER"].unique())
ethnicities = st.sidebar.multiselect("Select Ethnicity", options=stop_search_data["OFFICER_DEFINED_ETHNICITY"].unique())

# Aplicar os filtros
if genders:
    stop_search_data = stop_search_data[stop_search_data["GENDER"].isin(genders)]
if ethnicities:
    stop_search_data = stop_search_data[stop_search_data["OFFICER_DEFINED_ETHNICITY"].isin(ethnicities)]

# Mostrar os dados
st.dataframe(stop_search_data)

# Gráfico
fig = px.histogram(stop_search_data, x="GENDER", color="OUTCOME", barmode="group")
st.plotly_chart(fig)
