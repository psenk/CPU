from components.Memory import Memory

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
    'LDA_INY': 0xB1,
    # LDX
    'LDX_IMM': 0xA2,
    'LDX_ZPG': 0xA6,
    'LDX_ZPY': 0xB6,
    'LDX_ABS': 0xAE,
    'LDX_ABY': 0xBE,
    # LDY
    'LDY_IMM': 0xA0,
    'LDY_ZPG': 0xA4,
    'LDY_ZPX': 0xB4,
    'LDY_ABS': 0xAC,
    'LDY_ABX': 0xBC,
    # STA
    'STA_ZPG': 0x85,
    'STA_ZPX': 0x95,
    'STA_ABS': 0x8D,
    'STA_ABX': 0x9D,
    'STA_ABY': 0x99,
    'STA_INX': 0x81,
    'STA_INY': 0x91,
    # STX
    'STX_ZPG': 0x86,
    'STX_ZPY': 0x96,
    'STX_ABS': 0x8E,
    # STY
    'STY_ZPG': 0x84,
    'STY_ZPX': 0x94,
    'STY_ABS': 0x8C,

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

    def reset(self):
        self.pc = 0xFFFC
        self.sp = 0x0100

        self.a, self.x, self.y = 0, 0, 0

        self.c, self.z, self.i, self.d, self.b, self.v, self.n = 0, 0, 0, 0, 0, 0, 0

    def execute(self, expected_cycles):

        def consume_cycles(self, cycles):
            nonlocal expected_cycles
            self.taken_cycles += cycles
            expected_cycles -= cycles

        # fetch instruction each cycle
        while expected_cycles > 0:

            ins = self.fetch_byte()
            consume_cycles(self, 1)

            if ins == OP_CODES['LDA_IMM']:
                # load
                self.a = self.fetch_byte()
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.a = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPX']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.x
                consume_cycles(self, 1)

                # load
                self.a = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.a = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ABX']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                og_pg = addr & 0xFF00
                new_addr = addr + self.x
                # load
                self.a = self.read(new_addr)
                consume_cycles(self, 1)

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ABY']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                og_pg = addr & 0xFF00
                new_addr = addr + self.y
                # load
                self.a = self.read(new_addr)
                consume_cycles(self, 1)

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_INX']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr += self.x
                consume_cycles(self, 1)

                val_addr = self.fetch_bytes_from_location(loc=addr, bytes=2)
                consume_cycles(self, 2)

                # load
                self.a = self.read(val_addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_INY']:
                zp_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = self.fetch_bytes_from_location(loc=zp_addr, bytes=2)
                consume_cycles(self, 2)

                og_pg = addr & 0xFF00
                new_addr = addr + self.y

                # load
                self.a = self.read(new_addr)
                consume_cycles(self, 1)

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDX_IMM']:
                # load
                self.x = self.fetch_byte()
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDX_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.x = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDX_ZPY']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.y
                consume_cycles(self, 1)

                # load
                self.x = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDX_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.x = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDX_ABY']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                og_pg = addr & 0xFF00
                new_addr = addr + self.y
                # load
                self.x = self.read(new_addr)
                consume_cycles(self, 1)

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    consume_cycles(self, 1)

            elif ins == OP_CODES['LDY_IMM']:
                # load
                self.y = self.fetch_byte()
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDY_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.y = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDY_ZPX']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.x
                consume_cycles(self, 1)

                # load
                self.y = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDY_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.y = self.read(addr)
                consume_cycles(self, 1)

                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDY_ABX']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                og_pg = addr & 0xFF00
                new_addr = addr + self.x
                # load
                self.y = self.read(new_addr)
                consume_cycles(self, 1)

                new_pg = new_addr & 0xFF00
                if og_pg != new_pg:
                    consume_cycles(self, 1)

            elif ins == OP_CODES['STA_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_ZPX']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.x
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.memory.data[addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_ABX']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                new_addr = addr + self.x
                consume_cycles(self, 1)

                # load
                self.memory.data[new_addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_ABY']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                new_addr = addr + self.y
                consume_cycles(self, 1)

                # load
                self.memory.data[new_addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_INX']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr += self.x
                consume_cycles(self, 1)

                val_addr = self.fetch_bytes_from_location(loc=addr, bytes=2)
                consume_cycles(self, 2)

                # load
                self.memory.data[val_addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STA_INY']:
                zp_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = self.fetch_bytes_from_location(loc=zp_addr, bytes=2)
                consume_cycles(self, 2)

                new_addr = addr + self.y
                consume_cycles(self, 1)

                # load
                self.memory.data[new_addr] = self.a
                consume_cycles(self, 1)

            elif ins == OP_CODES['STX_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.x
                consume_cycles(self, 1)

            elif ins == OP_CODES['STX_ZPY']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.y
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.x
                consume_cycles(self, 1)

            elif ins == OP_CODES['STX_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.memory.data[addr] = self.x
                consume_cycles(self, 1)

            elif ins == OP_CODES['STY_ZPG']:
                addr = self.fetch_byte()
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.y
                consume_cycles(self, 1)

            elif ins == OP_CODES['STY_ZPX']:
                zero_page_addr = self.fetch_byte()
                consume_cycles(self, 1)

                addr = zero_page_addr + self.x
                consume_cycles(self, 1)

                # load
                self.memory.data[addr] = self.y
                consume_cycles(self, 1)

            elif ins == OP_CODES['STY_ABS']:
                addr = self.fetch_bytes(bytes=2)
                consume_cycles(self, 2)

                # load
                self.memory.data[addr] = self.y
                consume_cycles(self, 1)

            elif ins == OP_CODES['TEST']:
                pass

            else:
                print(f'Code not recognized: {ins}')
                self.b = 1


"""
ADDRESSING MODES

Immediate addressing - 2 cycles - LDA #10
1. fetch opcode
2. load value

Zero page addressing - 3 cycles - LDA $10
1. fetch opcode
2. fetch address (zero page)
3. load from address

Zero page + X addressing - 4 cycles, LDA $10,X
1. fetch opcode
2. fetch address (zero page)
3. add X to address
5. load from address

Absolute addressing - 4 cycles - LDA $00FF
1. fetch opcode
2-3. fetch address
4. load from address

Absolute + X/Y addressing - 4+1 cycles - LDA $2580,X
1. fetch opcode
2-3. fetch address
4. add X/Y to address, load from address
*5. if crossed pg

Indexed indirect addressing - 6 cycles - LDA ($20, X)
1. fetch opcode
2. fetch address of address
3. add X to address of address
4-5. fetch address
6. load from address

Indirect indexed addressing - 5+1 cycles - LDA ($20), Y
1. fetch opcode
2. fetch address of address
3-4. fetch address
5. add Y to address, load from address
*6. if crossed pg
"""
