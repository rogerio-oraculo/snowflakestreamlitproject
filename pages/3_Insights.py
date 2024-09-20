import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

st.title("Insights Combinados - Street y Stop and Search")

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
def load_combined_data():
    conn = get_snowflake_connection()
    query = """
    SELECT street.crime_type, street.latitude, street.longitude, stop.gender, stop.outcome
    FROM crimes_in_london_db.crimes_in_london_schema."table_street" AS street
    JOIN crimes_in_london_db.crimes_in_london_schema."table_stop_and_search" AS stop
    ON street.latitude = stop.latitude AND street.longitude = stop.longitude
    LIMIT 100;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados combinados
combined_data = load_combined_data()

# Mostrar os dados em um dataframe interativo
st.dataframe(combined_data)

# Gráfico combinado
fig = px.scatter(combined_data, x="CRIME_TYPE", y="OUTCOME", color="GENDER", title="Relación entre crímenes y búsquedas")
st.plotly_chart(fig)
