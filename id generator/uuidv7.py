import time
import random
import uuid

def generate_uuid7():
    # Obter o timestamp atual em milissegundos
    timestamp = int(time.time() * 1000)

    # Dividir o timestamp em partes altas e baixas
    time_high = (timestamp >> 28) & 0xFFFFF
    time_mid = (timestamp >> 12) & 0xFFFF
    time_low = timestamp & 0xFFF

    # Gerar os 4 bits de versão (0111 para versão 7)
    version = 0x7

    # Gerar os 62 bits restantes aleatórios
    rand_a = random.getrandbits(12)  # 12 bits
    rand_b = random.getrandbits(14)  # 14 bits
    rand_c = random.getrandbits(16)  # 16 bits
    rand_d = random.getrandbits(16)  # 16 bits

    # Montar o UUID v7
    time_hi_version = (version << 12) | (time_high & 0xFFF)
    clock_seq_hi_variant = (rand_a >> 4) & 0x3F
    clock_seq_low = rand_a & 0x0F

    uuid_fields = (
        time_low | (time_mid << 12),
        time_mid,
        time_hi_version,
        clock_seq_hi_variant | 0x80,  # Variância (sempre 10 para UUID v7)
        clock_seq_low,
        (rand_c << 16) | rand_d
    )

    return uuid.UUID(fields=uuid_fields)

# Lista para armazenar os UUIDs gerados
uuids = []

# Marca o tempo inicial
start_time = time.time()

# Gera 1.000.000 de UUIDs v7
for _ in range(1000000):
    uuids.append(generate_uuid7())

# Marca o tempo final
end_time = time.time()

# Calcula o tempo total levado
total_time = end_time - start_time

# Exibe o tempo total
print(f"Tempo total para gerar 1.000.000 de UUIDs v7: {total_time} segundos")
