import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Configurações da página
st.title("Street Crime Analysis in London")

# Função para obter a conexão com Snowflake via Snowpark
def get_snowflake_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

# Função para carregar dados usando Snowpark
@st.cache_data(ttl=600)
def load_street_data():
    session = get_snowflake_session()
    street_df = session.table('crimes_in_london_db.crimes_in_london_schema."table_street"')
    street_df = street_df.select("CRIME_TYPE", "LATITUDE", "LONGITUDE", "REPORTED_BY", "MONTH", "LOCATION")
    street_data = street_df.to_pandas()
    return street_data

# Carregar os dados
street_data = load_street_data()

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

# Remover as linhas que têm valores NaN em LATITUDE ou LONGITUDE
street_data = street_data.dropna(subset=['LATITUDE', 'LONGITUDE'])

if not street_data.empty:
    # Calcular o centro do mapa com base nos pontos filtrados
    avg_lat = street_data['LATITUDE'].mean()
    avg_lon = street_data['LONGITUDE'].mean()
    
    # Criar o mapa centrado nos dados filtrados
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
    # Adicionar marcadores ao mapa
    for _, data in street_data.iterrows():
        popup_info = f"""
            <div style="display: flex; flex-direction: row;">
                <div style="margin-right: 10px;"><b>Crime:</b> {data['CRIME_TYPE']}</div>
                <div><b>Location:</b> {data['LOCATION']}</div>
            </div>
        """
        latitude, longitude = data['LATITUDE'], data['LONGITUDE']
        folium.Marker(
            location=[latitude, longitude],
            icon=None,
            popup=folium.Popup(popup_info, max_width=400),
        ).add_to(marker_cluster)

    # Renderizar o mapa no Streamlit
    folium_static(m)
else:
    st.warning("Nenhum dado disponível para os filtros aplicados.")

# Função de paginação manual
def paginate_data(df, page_size):
    page_number = st.number_input("Page number", min_value=1, max_value=(len(df) // page_size) + 1, step=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    return df.iloc[start_idx:end_idx]

# Exibir a tabela abaixo do gráfico com paginação
page_size = 10
paginated_data = paginate_data(street_data, page_size)
st.dataframe(paginated_data, height=300)
