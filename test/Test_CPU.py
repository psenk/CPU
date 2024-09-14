import unittest
from components.CPU import CPU
from components.Memory import Memory


class Test_CPU(unittest.TestCase):

    def setUp(self):
        self.mem = Memory()
        self.cpu = CPU()

    def test_all_cpu_flags_false(self):

        self.assertFalse(self.cpu.c)
        self.assertFalse(self.cpu.z)
        self.assertFalse(self.cpu.i)
        self.assertFalse(self.cpu.d)
        self.assertFalse(self.cpu.b)
        self.assertFalse(self.cpu.v)
        self.assertFalse(self.cpu.n)

    if __name__ == '__main__':
        unittest.main()
