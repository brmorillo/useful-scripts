import os
import zipfile

def compress_season_folders(root_folder, delete_originals=False):
    # Listar todas as subpastas dentro da pasta raiz
    for subdir, _, files in os.walk(root_folder):
        # Ignorar a pasta raiz
        if subdir == root_folder:
            continue

        # Nome da subpasta (última parte do caminho)
        season_folder_name = os.path.basename(subdir)

        # Caminho do arquivo compactado a ser criado
        archive_name = os.path.join(subdir, season_folder_name)

        # Ignorar se já existir um arquivo compactado com o mesmo nome na pasta
        if os.path.exists(f"{archive_name}.zip"):
            print(f"O arquivo {archive_name}.zip já existe, ignorando.")
            continue

        # Criar o arquivo compactado dentro da pasta da temporada
        print(f"Compactando {subdir}...")

        # Lista para conter os arquivos a serem compactados (excluindo arquivos ZIP)
        files_to_zip = [f for f in files if not f.endswith('.zip')]

        with zipfile.ZipFile(f"{archive_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name in files_to_zip:
                absolute_file_path = os.path.join(subdir, file_name)
                zipf.write(absolute_file_path, file_name)

        print(f"Concluído: {archive_name}.zip")

        # Se delete_originals for True, deletar os arquivos originais
        if delete_originals:
            for file_name in files_to_zip:
                os.remove(os.path.join(subdir, file_name))
            print(f"Arquivos originais em {subdir} deletados.")

root_folder = "PATH"
delete_originals = False

compress_season_folders(root_folder, delete_originals)  # Mude para False se você não quer deletar os originais
