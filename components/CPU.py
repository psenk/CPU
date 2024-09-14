class CPU():

    # registers
    pc = None  # program counter
    sp = None  # stack pointer

    a = None   # accumulator
    x = None   # index register X
    y = None   # index register Y

    # processor status registers
    c = False  # carry flag
    z = False  # zero flag
    i = False  # interrupt disable
    d = False  # decimal mode
    b = False  # break command
    v = False  # overflow command
    n = False  # negative command

    def __init__(self):
        pass

    def reset(self):
        self.pc = 0xFFFC
        self.sp = 0x0100

        self.a, self.x, self.y = 0, 0, 0

        self.c, self.z, self.i, self.d, self.b, self.v, self.n = 0, 0, 0, 0, 0, 0, 0
