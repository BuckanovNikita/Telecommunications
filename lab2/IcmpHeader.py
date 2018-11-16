import struct


class IcmpHeader:
    ICMP_STRUCTURE_FMT = 'bbHHh'

    def __init__(self, icmp_type,
                 icmp_code=0,
                 icmp_crc=0,
                 icmp_id=1,
                 icmp_seq=1,
                 data=''):
        self.icmp_type = icmp_type
        self.icmp_code = icmp_code
        self.icmp_crc = icmp_crc
        self.icmp_id = icmp_id
        self.icmp_seq = icmp_seq
        self.data = data
        self.raw = None
        self.create_icmp_field()

    def create_icmp_field(self):
        self.raw = struct.pack(self.ICMP_STRUCTURE_FMT,
                               self.icmp_type,
                               self.icmp_code,
                               self.icmp_crc,
                               self.icmp_id,
                               self.icmp_seq,
                               )

        self.icmp_crc = IcmpHeader.crc(self.raw + self.data.encode())

        self.raw = struct.pack(self.ICMP_STRUCTURE_FMT,
                               self.icmp_type,
                               self.icmp_code,
                               self.icmp_crc,
                               self.icmp_id,
                               self.icmp_seq,
                               )

    @staticmethod
    def decode(data):
        x = str(struct.unpack(IcmpHeader.ICMP_STRUCTURE_FMT, data))
        return f'Type:{x[0]} Code:{x[1]} CRC:{x[2]} ID:{x[3]} Seq:{x[4]}'

    @staticmethod
    def crc(data):
        s = 0

        for i in range(0, len(data), 2):
            a = data[i]
            b = data[i+1]

            s = s + (a + (b << 8))

        s = s + (s >> 16)
        s = ~s & 0xffff

        return s
