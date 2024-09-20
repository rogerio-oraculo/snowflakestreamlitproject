import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

st.title("Combined Insights - Street and Stop and Search")

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
    SELECT street.CRIME_TYPE, street.LATITUDE, street.LONGITUDE, stop.GENDER, stop.OUTCOME, stop.DATE
    FROM crimes_in_london_db.crimes_in_london_schema."table_street" AS street
    JOIN crimes_in_london_db.crimes_in_london_schema."table_stop_and_search" AS stop
    ON street.LATITUDE = stop.LATITUDE AND street.LONGITUDE = stop.LONGITUDE;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados combinados
combined_data = load_combined_data()

# Converter a coluna 'DATE' para datetime
combined_data['DATE'] = pd.to_datetime(combined_data['DATE'])

# Criar a coluna de períodos do dia (manhã, tarde, noite, madrugada)
combined_data['TIME_OF_DAY'] = combined_data['DATE'].dt.hour.apply(
    lambda x: 'Early Morning' if 0 <= x < 6 else 
              'Morning' if 6 <= x < 12 else 
              'Afternoon' if 12 <= x < 18 else 
              'Evening'
)

# Filtros na barra lateral
crime_types = st.sidebar.multiselect("Select Crime Type", options=combined_data["CRIME_TYPE"].unique())
genders = st.sidebar.multiselect("Select Gender", options=combined_data["GENDER"].unique())

# Aplicar os filtros
if crime_types:
    combined_data = combined_data[combined_data["CRIME_TYPE"].isin(crime_types)]
if genders:
    combined_data = combined_data[combined_data["GENDER"].isin(genders)]

# Mostrar os dados
st.dataframe(combined_data)

# Gráfico dos horários com mais crimes
crime_time_fig = px.histogram(combined_data, x="TIME_OF_DAY", color="CRIME_TYPE", title="Crime Occurrences by Time of Day")
st.plotly_chart(crime_time_fig)

# Gráfico dos crimes mais frequentes por localização
crime_location_fig = px.scatter_mapbox(
    combined_data, lat="LATITUDE", lon="LONGITUDE", color="CRIME_TYPE", zoom=10,
    title="Most Frequent Crimes by Location"
)
crime_location_fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(crime_location_fig)

# Gráfico combinado
fig = px.scatter(combined_data, x="CRIME_TYPE", y="OUTCOME", color="GENDER", title="Relationship Between Crimes and Searches")
st.plotly_chart(fig)
