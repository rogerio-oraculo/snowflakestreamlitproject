import snowflake.connector
import os
import argparse
import streamlit as st

def create_snowflake_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )

def upload_file_to_stage(conn, file_path, stage_name):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
    
    upload_command = f"PUT file://{file_path} @{stage_name} AUTO_COMPRESS = FALSE"
    conn.cursor().execute(upload_command)
    
    print(f"Arquivo {file_path} carregado com sucesso para a stage @{stage_name}.")

def list_stage_files(conn, stage_name):
    cursor = conn.cursor()
    cursor.execute(f"LIST @{stage_name}")
    files = cursor.fetchall()
    if not files:
        print(f"Nenhum arquivo encontrado na stage @{stage_name}.")
    else:
        print(f"Arquivos na stage @{stage_name}:")
        for file in files:
            print(file)

def main():
    parser = argparse.ArgumentParser(description="Upload de arquivos CSV para uma stage no Snowflake.")
    parser.add_argument('--file', required=True, help="Caminho para o arquivo CSV local que será enviado.")
    parser.add_argument('--stage', required=True, help="Nome da stage no Snowflake.")
    
    args = parser.parse_args()
    
    conn = create_snowflake_connection()
    
    try:
        upload_file_to_stage(conn, args.file, args.stage)
        
        list_stage_files(conn, args.stage)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
