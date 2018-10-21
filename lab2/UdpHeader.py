class UdpHeader:
    def __init__(self, bits):
        self.source_port = int(bits[0:16].to01(), 2)
        self.destination_port = int(bits[16:32].to01(), 2)
        self.datagram_size = int(bits[32:48].to01(), 2)
        self.crc = bits[48:64].tobytes().hex()
        self.data = bits[64:].tobytes().hex()

    def __str__(self):
        return f"Source port: {self.source_port}\n" \
               f"Destination port: {self.destination_port}\n" \
               f"CRC: {self.crc}\n"
