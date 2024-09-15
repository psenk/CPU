from components.Memory import Memory

OP_CODES = {
    'LDA_IMM': 0xA9,
    'LDA_ZPG': 0xA5,
    'LDA_ZPX': 0xB5
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

    def reset(self):
        self.pc = 0xFFFC
        self.sp = 0x0100

        self.a, self.x, self.y = 0, 0, 0

        self.c, self.z, self.i, self.d, self.b, self.v, self.n = 0, 0, 0, 0, 0, 0, 0

    def fetch(self):
        # multi-byte instructions?
        instruction = self.memory.data[self.pc]
        self.pc += 1
        return instruction

    def read(self, address):
        instruction = self.memory.data[address]
        return instruction

    def load(self, cycles, location, data):
        self.memory.data[location] = data
        self.pc += 1
        cycles -= 1

    def execute(self, cycles):

        # fetch instruction each cycle
        while cycles > 0:

            ins = self.fetch()
            cycles -= 1

            if ins == OP_CODES['LDA_IMM']:
                data = self.fetch()
                cycles -= 1
                self.a = data
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPG']:
                zero_page_addr = self.fetch()
                cycles -= 1
                val = self.read(zero_page_addr)  # reading takes no cycles
                self.a = val
                cycles -= 1
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            elif ins == OP_CODES['LDA_ZPX']:
                zero_page_addr = self.fetch()
                cycles -= 1
                addr = zero_page_addr + self.x
                cycles -= 1
                val = self.read(addr)
                self.a = val
                cycles -= 1
                self.z = 1 if self.a == 0 else 0
                self.n = 1 if (self.a & 0x80) != 0 else 0

            else:
                print('Code not recognized.')
