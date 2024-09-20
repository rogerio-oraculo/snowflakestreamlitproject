import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.title("Street Crime Analysis in London")

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
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_street";"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados
street_data = load_street_data()
street_data = street_data.drop(columns=["CRIME_ID", "CONTEXT"])

# Filtros na barra lateral
crime_types = st.sidebar.multiselect("Select Crime Type", options=street_data["CRIME_TYPE"].unique())
regions = st.sidebar.multiselect("Select Region", options=street_data["REPORTED_BY"].unique())
months = st.sidebar.multiselect("Select Month", options=street_data["MONTH"].unique())

# Aplicar os filtros
if crime_types:
    street_data = street_data[street_data["CRIME_TYPE"].isin(crime_types)]
if regions:
    street_data = street_data[street_data["REPORTED_BY"].isin(regions)]
if months:
    street_data = street_data[street_data["MONTH"].isin(months)]

# Verificar se as colunas 'LATITUDE', 'LONGITUDE' e 'LOCATION' existem
if 'LATITUDE' in street_data.columns and 'LONGITUDE' in street_data.columns and 'LOCATION' in street_data.columns:
    fig = px.scatter_mapbox(
        street_data, 
        lat="LATITUDE", 
        lon="LONGITUDE", 
        color="CRIME_TYPE", 
        zoom=10, 
        hover_data={"LATITUDE": False, "LONGITUDE": False, "LOCATION": True},
        size_max=15
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)
else:
    st.warning("As colunas 'LATITUDE', 'LONGITUDE' e 'LOCATION' não estão disponíveis no conjunto de dados.")

# Paginação manual
def paginate_data(df, page_size):
    page_number = st.number_input("Page number", min_value=1, max_value=(len(df) // page_size) + 1, step=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    return df.iloc[start_idx:end_idx]

# Exibir a tabela abaixo do gráfico com paginação
page_size = 10
paginated_data = paginate_data(street_data, page_size)
st.dataframe(paginated_data, height=300)
