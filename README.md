# Crimes em Londres

## Criar Ambiente Virtual
````
python3 -m venv crimes_in_london_venv
````
## Instalar conector Snowflake
````
pip3 install snowflake-connector-python
````
## Upload para a stage do snowflake
````
python3 upload_to_snowflake.py --file incoming/2024-07/2024-07-city-of-london-street.csv --stage CRIMES_IN_LONDON_STAGE
python3 upload_to_snowflake.py --file incoming/2024-07/2024-07-city-of-london-stop-and-search.csv --stage CRIMES_IN_LONDON_STAGE
````
## Criar tabelas csom base nos arquivos da Stage
(...)


