from components.Memory import Memory

"""
Indexed indirect addressing - 6 cycles - LDA ($20, X)

Indirect indexed addressing - 5+1 cycles - LDA ($20), Y

"""

OP_CODES = {
    'TEST': 'X',
    # LDA
    'LDA_IMM': 0xA9,
    'LDA_ZPG': 0xA5,
    'LDA_ZPX': 0xB5,
    'LDA_ABS': 0xAD,
    'LDA_ABX': 0xBD,
    'LDA_ABY': 0xB9,
    'LDA_INX': 0xA1,
    'LDA_INY': 0xB1
    # LDX
}

"""
0x0000 - 0x00FF = zero page
"""


class CPU():

    def __init__(self):
        # registers
        self.pc = 0  # program counter
        self.sp = 0  # stack pointer

        self.a = 0   # accumulator
        self.x = 0   # index register X
        self.y = 0   # index register Y

        # processor status registers
        self.c = 0  # carry flag
        self.z = 0  # zero flag
        self.i = 0  # interrupt disable
        self.d = 0  # decimal mode
        self.b = 0  # break command
        self.v = 0  # overflow command
        self.n = 0  # negative number

        self.memory = Memory()

        # test use
        self.taken_cycles = 0

    def reset(self):
        self.pc = 0xFFFC
        self.sp = 0x0100

        self.a, self.x, self.y = 0, 0, 0

        self.c, self.z, self.i, self.d, self.b, self.v, self.n = 0, 0, 0, 0, 0, 0, 0

    def fetch_byte(self):
        val = self.memory.data[self.pc]
        self.pc += 1
        return val

    def fetch_bytes(self, bytes):
        val = 0
        for _ in range(bytes):
            val |= self.memory.data[self.pc] << (8 * _)
            self.pc += 1
        return val

    def fetch_bytes_from_location(self, loc, bytes):
        val = 0
        for _ in range(bytes):
            val |= self.memory.data[loc] << (8 * _)
            loc += 1
        return val

    def read(self, address):
        instruction = self.memory.data[address]
        return instruction

    def execute(self, expected_cycles):

        # fetch instruction each cycle
        while expected_cycles > 0:

            ins = self.fetch_byte()
            expected_cycles -= 1
            self.taken_cycles += 1

            if ins == OP_CODES['LDA_IMM']:
                data = self.fetch_byte()
                expected_cycles -= 1
                self.taken_cycles += 1

                self.a = data
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPG']:
                zero_page_addr = self.fetch_byte()
                expected_cycles -= 1
                self.taken_cycles += 1
                val = self.read(zero_page_addr)  # reading takes no cycles
                self.a = val
                expected_cycles -= 1
                self.taken_cycles += 1
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPX']:
                zero_page_addr = self.fetch_byte()
                expected_cycles -= 1
                self.taken_cycles += 1
                addr = zero_page_addr + self.x
                expected_cycles -= 1
                self.taken_cycles += 1
                val = self.read(addr)
                self.a = val
                expected_cycles -= 1
                self.taken_cycles += 1
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ABS']:
                addr = self.fetch_bytes(bytes=2)
                expected_cycles -= 2
                self.taken_cycles += 2
                val = self.read(addr)
                self.a = val
                expected_cycles -= 1
                self.taken_cycles += 1
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ABX']:
                addr = self.fetch_bytes(bytes=2)
                expected_cycles -= 2
                self.taken_cycles += 2

                og_pg = addr & 0xFF00
                new_addr = addr + self.x
                self.a = self.read(new_addr)
                expected_cycles -= 1
                self.taken_cycles += 1

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    expected_cycles -= 1
                    self.taken_cycles += 1

            elif ins == OP_CODES['LDA_ABY']:
                addr = self.fetch_bytes(bytes=2)
                expected_cycles -= 2
                self.taken_cycles += 2

                og_pg = addr & 0xFF00
                new_addr = addr + self.y
                self.a = self.read(new_addr)
                expected_cycles -= 1
                self.taken_cycles += 1

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    expected_cycles -= 1
                    self.taken_cycles += 1

            elif ins == OP_CODES['LDA_INX']:
                addr = self.fetch_byte()
                expected_cycles -= 1
                self.taken_cycles += 1

                addr += self.x
                expected_cycles -= 1
                self.taken_cycles += 1

                val_addr = self.fetch_bytes_from_location(loc=addr, bytes=2)
                expected_cycles -= 2
                self.taken_cycles += 2

                self.a = self.read(val_addr)
                expected_cycles -= 1
                self.taken_cycles += 1

            elif ins == OP_CODES['LDA_INY']:
                zp_addr = self.fetch_byte()
                expected_cycles -= 1
                self.taken_cycles += 1

                addr = self.fetch_bytes_from_location(loc=zp_addr, bytes=2)
                expected_cycles -= 2
                self.taken_cycles += 2

                og_pg = addr & 0xFF00
                new_addr = addr + self.y
                self.a = self.read(new_addr)
                expected_cycles -= 1
                self.taken_cycles += 1

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    expected_cycles -= 1
                    self.taken_cycles += 1

            elif ins == OP_CODES['TEST']:
                pass

            else:
                print(f'Code not recognized: {ins}')
                raise ValueError


