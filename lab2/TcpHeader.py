from bitarray import bitarray


class TcpHeader:
    def __init__(self, bits):
        # self.original = bytes_.hex()
        # bits = bitarray(endian='big')
        # bits.frombytes(bytes_)
        self.source_port = int(bits[0:16].to01(), 2)
        self.destination_port = int(bits[16:32].to01(), 2)
        self.sn = int(bits[32:64].to01(), 2)
        self.ack_sn = int(bits[64:96].to01(), 2)
        self.header_size = int(bits[96:100].to01(), 2)
        self.reserved = int(bits[100:106].to01(), 2)
        self.flags = bits[106:112].to01()
        self.frame_size = int(bits[112:128].to01(), 2)
        self.crc = bits[128:144].tobytes().hex()
        self.priority = int(bits[144:160].to01(), 2)
        self.options = bits[160:32 * self.header_size].tobytes().hex()

    def __str__(self):
        return f"Source port: {self.source_port}\n" \
               f"Destination port: {self.destination_port}\n" \
               f"SN: {self.sn}\n" \
               f"ACK SN: {self.ack_sn}\n" \
               f"Header size: {self.header_size}\n" \
               f"Reserved: {self.reserved}\n" \
               f"Flags: {self.flags}\n" \
               f"Frame size: {self.frame_size}\n" \
               f"CRC: {self.crc}\n" \
               f"Priority: {self.priority}\n" \
               f"TCP Options: {self.options}\n"
