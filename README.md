# Criar Ambiente Virtual

python3 -m venv crimes_in_london_venv

# Instalar conector Snowflake

pip3 install snowflake-connector-python

# Upload para a stage do snowflake

python3 upload_to_snowflake.py --file incoming/2024-07/2024-07-city-of-london-street.csv --stage CRIMES_IN_LONDON_STAGE
python3 upload_to_snowflake.py --file incoming/2024-07/2024-07-city-of-london-stop-and-search.csv --stage CRIMES_IN_LONDON_STAGE

# Criar tabelas com base nos arquivos da Stage

Pode converter o connection.json para secrets.toml no padrão streamlist/snowflake:

{
    "account"   : "PVGCNRR-RXB73171",
    "user"      : "rogerioelquinto",
    "password"  : "ZeOmbro@2024",
    "role"      : "ACCOUNTADMIN",
    "warehouse" : "COMPUTE_WH",
    "database"  : "CRIMES_IN_LONDON_DB",
    "schema"    : "CRIMES_IN_LONDON_SCHEMA"
  }

  segundo as instruções em https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management