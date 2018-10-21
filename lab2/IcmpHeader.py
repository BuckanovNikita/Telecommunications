class IcmpHeader:
    def __init__(self, bits):
        self.type = int(bits[0:8].to01(), 2)
        self.code = int(bits[8:16].to01(), 2)
        self.crc = bits[16:24].tobytes().hex()
        self.data = bits[24:].tobytes().hex()

    def __str__(self):
        return f'ICMP type: {self.type}\n'\
               f'ICMP code: {self.code}\n'\
               f'CRC: {self.crc}\n' \
