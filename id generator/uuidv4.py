import time
import uuid

# Lista para armazenar os UUIDs gerados
uuids = []

# Marca o tempo inicial
start_time = time.time()

# Gera 1.000.000 de UUIDs v4
for _ in range(1000000):
    uuids.append(uuid.uuid4())

# Marca o tempo final
end_time = time.time()

# Calcula o tempo total levado
total_time = end_time - start_time

# Exibe o tempo total
print(f"Tempo total para gerar 1.000.000 de UUIDs v4: {total_time} segundos")
