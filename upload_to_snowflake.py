import snowflake.connector
import json
import os
import argparse

def load_connection_config():
    """Carrega as credenciais de conexão do arquivo connection.json."""
    with open('connection.json', 'r') as f:
        return json.load(f)

def create_snowflake_connection(config):
    """Cria uma conexão com o Snowflake usando as credenciais."""
    return snowflake.connector.connect(
        user=config['user'],
        password=config['password'],
        account=config['account'],
        warehouse=config['warehouse'],
        database=config['database'],
        schema=config['schema'],
        role=config['role']
    )

def upload_file_to_stage(conn, file_path, stage_name):
    """Faz upload de um arquivo local para uma stage no Snowflake."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
    
    # Comando PUT com AUTO_COMPRESS = FALSE
    upload_command = f"PUT file://{file_path} @{stage_name} AUTO_COMPRESS = FALSE"
    conn.cursor().execute(upload_command)
    
    print(f"Arquivo {file_path} carregado com sucesso para a stage @{stage_name}.")

def list_stage_files(conn, stage_name):
    """Lista os arquivos presentes na stage."""
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
    
    # Carrega as credenciais de conexão diretamente do connection.json
    config = load_connection_config()
    
    # Cria uma conexão com o Snowflake
    conn = create_snowflake_connection(config)
    
    try:
        # Upload do arquivo para a stage
        upload_file_to_stage(conn, args.file, args.stage)
        
        # Listar arquivos na stage
        list_stage_files(conn, args.stage)
    finally:
        # Fechar a conexão
        conn.close()

if __name__ == "__main__":
    main()
