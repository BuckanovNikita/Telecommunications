from bitarray import bitarray


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
        self.original = bits

        self.source_address = [int(bits[96:104].to01(), 2),
                               int(bits[104:112].to01(), 2),
                               int(bits[112:120].to01(), 2),
                               int(bits[120:128].to01(), 2)]

        self.destination_address = [int(bits[128:136].to01(), 2),
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

    def __str__(self):
        ip1 = ''
        for t in self.source_address:
            ip1 = ip1 + str(t)+':'
        ip1 = ip1[:-1]

        ip2 = ''
        for t in self.destination_address:
            ip2 = ip2 + str(t) + ':'
        ip2 = ip2[:-1]

        options_str = ''
        for t in self.options:
            options_str += str(t)

        return f'RAW content: {self.original.tobytes().hex()}\n'\
               f'IP version: {self.version}\n' \
               f'Header size: {self.header_size}\n'\
               f'DSCP: {self.dscp}\n'\
               f'ECN: {self.ecn}\n'\
               f'Package size: {self.full_size}\n'\
               f'ID: {self.id}\n'\
               f'Flags: {self.flags}\n'\
               f'Margin:{self.margin}\n'\
               f'TTL: {self.ttl}\n'\
               f'Protocol: {self.protocol}\n'\
               f'CRC32: {self.crc}\n'\
               f'Source IP: {ip1}\n'\
               f'Destination IP: {ip2}\n'\
               f'Options: {options_str}\n'\
               f'Data: {self.data.tobytes().hex()}'
        

class Option:
    def __init__(self, type_, size=0, args=None):
        self.type = type_
        self.size = size
        self.args = args

    def __str__(self):
        return f'Type: {self.type_}\n'\
               f'Size: {self.size}\n'\
               f'Args: {self.args}\n'
