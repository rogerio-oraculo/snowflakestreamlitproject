import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from snowflake.snowpark import Session

st.title("Street Crime Analysis in London")

def get_snowflake_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

@st.cache_data(ttl=600)
def load_street_data():
    session = get_snowflake_session()
    street_df = session.table('crimes_in_london_db.crimes_in_london_schema."table_street"')
    street_df = street_df.select("CRIME_TYPE", "LATITUDE", "LONGITUDE", "REPORTED_BY", "MONTH", "LOCATION")
    street_data = street_df.to_pandas()
    return street_data

street_data = load_street_data()

crime_types = st.sidebar.multiselect("Select Crime Type", options=street_data["CRIME_TYPE"].unique())
locations = st.sidebar.multiselect("Select Location", options=street_data["LOCATION"].unique())
months = st.sidebar.multiselect("Select Month", options=street_data["MONTH"].unique())

if crime_types:
    street_data = street_data[street_data["CRIME_TYPE"].isin(crime_types)]
if locations:
    street_data = street_data[street_data["LOCATION"].isin(locations)]
if months:
    street_data = street_data[street_data["MONTH"].isin(months)]

street_data = street_data.dropna(subset=['LATITUDE', 'LONGITUDE'])

if not street_data.empty:
    avg_lat = street_data['LATITUDE'].mean()
    avg_lon = street_data['LONGITUDE'].mean()
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
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

    folium_static(m)
else:
    st.warning("Nenhum dado disponível para os filtros aplicados.")

def paginate_data(df, page_size):
    page_number = st.number_input("Page number", min_value=1, max_value=(len(df) // page_size) + 1, step=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    return df.iloc[start_idx:end_idx]

street_data = street_data.drop(columns=["REPORTED_BY"])

page_size = 10
paginated_data = paginate_data(street_data, page_size)
st.dataframe(paginated_data, height=300)
