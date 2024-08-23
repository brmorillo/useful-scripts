import os
import subprocess
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

# Configuração do log
logging.basicConfig(
    filename="backup_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Lista de conexões de banco de dados
databases = [
    {
        "name": "",
        "user": "",
        "pass": "",
        "default_db": "",
        "host": "",
    },
]


def pg_dump_db(db_info):
    db_name = db_info["default_db"]
    db_user = db_info["user"]
    db_pass = db_info["pass"]
    db_host = db_info["host"]

    # Criar o diretório para salvar o backup
    backup_dir = os.path.join("./backups", db_info["name"])
    os.makedirs(backup_dir, exist_ok=True)

    # Construir o nome do arquivo de backup com a data e hora atual
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{current_datetime}.dump")

    # Comando para pg_dump
    command = f'PGPASSWORD="{db_pass}" pg_dump -h {db_host} -U {db_user} -d {db_name} -F c -f {backup_file}'

    try:
        # Executar o comando no terminal
        subprocess.run(command, shell=True, check=True)
        logging.info(
            f"Backup do banco de dados {db_name} realizado com sucesso em {backup_file}"
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao realizar backup do banco de dados {db_name}: {e}")


# Função para paralelizar os backups
def execute_backups():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(pg_dump_db, databases)


if __name__ == "__main__":
    execute_backups()
