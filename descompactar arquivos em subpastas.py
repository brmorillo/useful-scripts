import os
import zipfile

def unzip_and_delete(directory, delete_zip=False):
    # Caminha por todos os diretórios e subdiretórios
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.zip'):  # Verifica se o arquivo é um .zip
                zip_filepath = os.path.join(dirpath, filename)  # Caminho completo do arquivo .zip
                unzip_dir = dirpath  # Diretório onde o .zip será descompactado

                # Informa o arquivo que está sendo descompactado
                print(f"Iniciando descompactação do zip {filename} ...", end='')

                # Descompacta o arquivo
                with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                    zip_ref.extractall(unzip_dir)

                print(f"Finalizado descompactação do zip.", end='\r')

                # Deleta o arquivo .zip se delete_zip for True
                if delete_zip:
                    print(f"Deletando {filename} ...")
                    os.remove(zip_filepath)
                else:
                    print("")

# Uso da função
directory = "PATH"  # Substitua com o caminho do diretório onde você quer começar
delete_zip = False  # True se você quer deletar os arquivos .zip após descompactação, False caso contrário

unzip_and_delete(directory, delete_zip)
