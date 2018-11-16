from bitarray import bitarray
from IcmpHeader import IcmpHeader
from TcpHeader import TcpHeader
from UdpHeader import UdpHeader
import re

class IPPackage:

    def __init__(self, bytes_):
        self.original = bytes_.hex()
        bits = bitarray(endian='big')
        bits.frombytes(bytes_)
        self.version = int(bits[0:4].to01(), 2)
        self.header_size = int(bits[4:8].to01(), 2)
        self.dscp = int(bits[8:14].to01(), 2)
        self.ecn = int(bits[14:16].to01(), 2)
        self.full_size = int(bits[16:32].to01(), 2)
        self.id = int(bits[32:48].to01(), 2)
        self.flags = bits[48:51].to01()
        self.margin = int(bits[51:64].to01(), 2)
        self.ttl = int(bits[64:72].to01(), 2)
        self.protocol = int(bits[72:80].to01(), 2)
        self.crc = bits[80:96].tobytes().hex()
        self.data = bits[self.header_size * 32:]

        source_address = [int(bits[96:104].to01(), 2),
                          int(bits[104:112].to01(), 2),
                          int(bits[112:120].to01(), 2),
                          int(bits[120:128].to01(), 2)]

        destination_address = [int(bits[128:136].to01(), 2),
                               int(bits[136:144].to01(), 2),
                               int(bits[144:152].to01(), 2),
                               int(bits[152:160].to01(), 2)]
        self.options = []

        if self.header_size > 5:
            i = 160
            while i + 8 <= self.header_size * 32:
                option_type = int(bits[i:i + 8].to01(), 2)
                if not bits[i + 8:i + 16].to01() == '':
                    option_size = int(bits[i + 8:i + 16].to01(), 2)
                else:
                    option_size = 0
                option_args = None
                if option_size:
                    option_args = bits[i + 16:i + option_size].tobytes().hex()
                i += max(8, option_size)
                self.options.append(Option(option_type, option_size, option_args))

        self.source_ip = ''
        for t in source_address:
            self.source_ip = self.source_ip + str(t) + ':'
        self.source_ip = self.source_ip[:-1]

        self.destination_ip = ''
        for t in destination_address:
            self.destination_ip = self.destination_ip + str(t) + ':'
        self.destination_ip = self.destination_ip[:-1]

        self.options_str = ''
        for t in self.options:
            self.options_str += str(t)

        if self.protocol == 6:
            self.header = str(TcpHeader(self.data))
        elif self.protocol == 17:
            self.header = str(UdpHeader(self.data))
        elif self.protocol == 1:
            self.header = IcmpHeader.decode(self.data.tobytes())
        else:
            self.header = ''

        raw_content = self.original
        raw_content = re.findall('..', raw_content)
        self.raw_str = '\n'

        for i, t in enumerate(raw_content):
            self.raw_str += t + ' '
            if i > 0 and i % 40 == 0:
                self.raw_str += '\n'

        self.ascii_str = '\n'
        for i, t in enumerate(raw_content):
            try:
                self.ascii_str += bytes.fromhex(t).decode('utf-8')
            except Exception as e:
                self.ascii_str += ''
            if i > 0 and i % 40 == 0:
                self.ascii_str += '\n'

    def __str__(self):
        return f"IP version: {self.version}\n" \
               f"Header size: {self.header_size}    " \
               f"DSCP: {self.dscp}\n" \
               f"ECN: {self.ecn}    " \
               f"Package size: {self.full_size}\n" \
               f"ID: {self.id}  " \
               f"Flags: {self.flags}\n" \
               f"Margin:{self.margin}   " \
               f"TTL: {self.ttl}\n" \
               f"Protocol: {self.protocol}  " \
               f"CRC32: {self.crc}\n" \
               f"Source IP: {self.source_ip}    " \
               f"Destination IP: {self.destination_ip}\n" \
               f"Content header:\n {self.header}\n"
        

class Option:
    def __init__(self, type_, size=0, args=None):
        self.type = type_
        self.size = size
        self.args = args

    def __str__(self):
        return f'Type: {self.type}\n'\
               f'Size: {self.size}\n'\
               f'Args: {self.args}\n'
