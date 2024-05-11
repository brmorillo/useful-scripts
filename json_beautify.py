import json
import os
import sys

def format_json(input_path):
    # Verifica se o arquivo existe
    if not os.path.isfile(input_path):
        print(f"Arquivo não encontrado: {input_path}")
        return
    
    # Determina o caminho de saída baseado no caminho de entrada e sua extensão
    base, ext = os.path.splitext(input_path)
    output_path = base + ".json" if ext != ".json" else base + "_2.json"
    
    try:
        # Abre e lê o arquivo de entrada
        with open(input_path, 'r', encoding='utf-8') as file:
            # Carrega o conteúdo como um objeto JSON
            data = json.load(file)
        
        # Abre o arquivo de saída e escreve o JSON formatado
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        print(f"Arquivo processado e salvo como: {output_path}")

    except json.JSONDecodeError:
        print(f"Erro ao ler o JSON no arquivo: {input_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <caminho_do_arquivo>")
    else:
        format_json(sys.argv[1])
