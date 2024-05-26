import time
import random

BASE32_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def encode_base32hex(input_bytes):
    """Encode bytes to a Base32 string using the Crockford's alphabet."""
    encoded = []
    for byte in input_bytes:
        encoded.append(BASE32_ALPHABET[(byte >> 3) & 0x1F])
        encoded.append(BASE32_ALPHABET[(byte << 2) & 0x1C | (byte >> 6) & 0x03])
    return ''.join(encoded)

def encode_time(timestamp):
    """Encode timestamp (in ms) to 10 character ULID string."""
    return encode_base32hex(timestamp.to_bytes(6, byteorder='big'))

def encode_random(random_value):
    """Encode random value to 16 character ULID string."""
    return encode_base32hex(random_value.to_bytes(10, byteorder='big'))

def generate_ulid():
    """Generate a ULID string."""
    # Current timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Random part (80 bits)
    random_value = random.getrandbits(80)

    # Encode timestamp and random part
    ulid_str = encode_time(timestamp) + encode_random(random_value)

    return ulid_str

# Lista para armazenar os ULIDs gerados
ulids = []

# Marca o tempo inicial
start_time = time.time()

# Gera 1.000.000 de ULIDs
for _ in range(1000000):
    ulids.append(generate_ulid())

# Marca o tempo final
end_time = time.time()

# Calcula o tempo total levado
total_time = end_time - start_time

# Exibe o tempo total
print(f"Tempo total para gerar 1.000.000 de ULIDs: {total_time} segundos")
