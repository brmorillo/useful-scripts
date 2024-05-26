import time

class SnowflakeIDGenerator:
    def __init__(self, worker_id, datacenter_id, sequence=0):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.epoch = 1288834974657  # Época base (Twitter)
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.sequence_bits = 12

        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

        self.last_timestamp = -1

    def _time_gen(self):
        return int(time.time() * 1000)

    def _till_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def next_id(self):
        timestamp = self._time_gen()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id")

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return ((timestamp - self.epoch) << self.timestamp_left_shift) | \
               (self.datacenter_id << self.datacenter_id_shift) | \
               (self.worker_id << self.worker_id_shift) | \
               self.sequence

# Configuração do gerador de Snowflake IDs
worker_id = 1
datacenter_id = 1
generator = SnowflakeIDGenerator(worker_id, datacenter_id)

# Lista para armazenar os IDs gerados
ids = []

# Marca o tempo inicial
start_time = time.time()

# Gera 1.000.000 de Snowflake IDs
for _ in range(1000000):
    ids.append(generator.next_id())

# Marca o tempo final
end_time = time.time()

# Calcula o tempo total levado
total_time = end_time - start_time

# Exibe o tempo total
print(f"Tempo total para gerar 1.000.000 de Snowflake IDs: {total_time} segundos")
