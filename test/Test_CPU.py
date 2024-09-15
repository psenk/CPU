import unittest
from components.CPU import CPU


class Test_CPU(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    def set_all_flags_on(self):
        self.cpu.c, self.cpu.z, self.cpu.i, self.cpu.d, self.cpu.b, self.cpu.v, self.cpu.n = 1, 1, 1, 1, 1, 1, 1

    def set_all_flags_off(self):
        self.cpu.c, self.cpu.z, self.cpu.i, self.cpu.d, self.cpu.b, self.cpu.v, self.cpu.n = 0, 0, 0, 0, 0, 0, 0

    def test_all_cpu_flags_off(self):

        self.assertEquals(self.cpu.c, 0)
        self.assertEquals(self.cpu.z, 0)
        self.assertEquals(self.cpu.i, 0)
        self.assertEquals(self.cpu.d, 0)
        self.assertEquals(self.cpu.b, 0)
        self.assertEquals(self.cpu.v, 0)
        self.assertEquals(self.cpu.n, 0)

    def test_all_cpu_flags_on_func(self):

        self.set_all_flags_on()

        self.assertEquals(self.cpu.c, 1)
        self.assertEquals(self.cpu.z, 1)
        self.assertEquals(self.cpu.i, 1)
        self.assertEquals(self.cpu.d, 1)
        self.assertEquals(self.cpu.b, 1)
        self.assertEquals(self.cpu.v, 1)
        self.assertEquals(self.cpu.n, 1)

    def test_cpu_reset(self):

        self.pc = 0x0000
        self.sp = 0x0000

        self.cpu.x = 24
        self.cpu.y = 56
        self.cpu.a = 22

        self.set_all_flags_on()
        self.cpu.reset()

        self.assertEquals(self.cpu.pc, 0xFFFC)
        self.assertEquals(self.cpu.sp, 0x0100)

        self.assertEquals(self.cpu.x, 0)
        self.assertEquals(self.cpu.y, 0)
        self.assertEquals(self.cpu.z, 0)

        self.test_all_cpu_flags_off()

    def test_taken_cycles_correct(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 'X'
        self.cpu.memory.data[0xFFFD] = 'X'
        self.cpu.memory.data[0xFFFE] = 'X'

        self.cpu.execute(3)

        self.assertEquals(self.cpu.taken_cycles, 3)

    def test_load_a_immediate(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA9
        self.cpu.memory.data[0xFFFD] = 0x42

        self.cpu.execute(2)

        self.assertEquals(self.cpu.a, 0x42)

    def test_load_a_immediate_negative(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA9
        self.cpu.memory.data[0xFFFD] = 0xFB

        self.cpu.execute(2)

        self.assertEquals(self.cpu.a, 0xFB)
        self.assertEquals(self.cpu.n, 1)

    def test_load_a_immediate_zero(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA9
        self.cpu.memory.data[0xFFFD] = 0

        self.cpu.execute(2)

        self.assertEquals(self.cpu.a, 0)
        self.assertEquals(self.cpu.z, 1)

    def test_load_a_zero_page(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA5
        self.cpu.memory.data[0xFFFD] = 0x10
        self.cpu.memory.data[0x10] = 0x42

        self.cpu.execute(3)
        self.assertEquals(self.cpu.a, 0x42)

    def test_load_a_zero_page_negative(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA5
        self.cpu.memory.data[0xFFFD] = 0x10
        self.cpu.memory.data[0x10] = 0xFB

        self.cpu.execute(3)
        self.assertEquals(self.cpu.a, 0xFB)
        self.assertEquals(self.cpu.n, 1)

    def test_load_a_zero_page_zero(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA5
        self.cpu.memory.data[0xFFFD] = 0x10
        self.cpu.memory.data[0x10] = 0

        self.cpu.execute(3)
        self.assertEquals(self.cpu.a, 0)
        self.assertEquals(self.cpu.z, 1)

    def test_load_a_zero_page_x(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xB5
        self.cpu.memory.data[0xFFFD] = 0x80
        self.cpu.x = 0x0F
        self.cpu.memory.data[0x008F] = 0x42

        self.cpu.execute(4)
        self.assertEquals(self.cpu.a, 0x42)

    def test_load_a_absolute(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xAD
        self.cpu.memory.data[0xFFFD] = 0x80
        self.cpu.memory.data[0xFFFE] = 0x25
        self.cpu.memory.data[0x2580] = 0x42

        self.cpu.execute(4)
        self.assertEquals(self.cpu.a, 0x42)

    def test_load_a_absolute_x(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xBD
        self.cpu.memory.data[0xFFFD] = 0x80
        self.cpu.memory.data[0xFFFE] = 0x25
        self.cpu.x = 0x01
        self.cpu.memory.data[0x2581] = 0x42

        self.cpu.execute(4)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 4)

    def test_load_a_absolute_x_page_boundary_crossed(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xBD
        self.cpu.memory.data[0xFFFD] = 0x02
        self.cpu.memory.data[0xFFFE] = 0x44
        self.cpu.x = 0xFF
        self.cpu.memory.data[0x4501] = 0x42

        self.cpu.execute(5)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 5)

    def test_load_a_absolute_y(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xB9
        self.cpu.memory.data[0xFFFD] = 0x80
        self.cpu.memory.data[0xFFFE] = 0x25
        self.cpu.y = 0x01
        self.cpu.memory.data[0x2581] = 0x42

        self.cpu.execute(4)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 4)

    def test_load_a_absolute_y_page_boundary_crossed(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xB9
        self.cpu.memory.data[0xFFFD] = 0x02
        self.cpu.memory.data[0xFFFE] = 0x44
        self.cpu.y = 0xFF
        self.cpu.memory.data[0x4501] = 0x42

        self.cpu.execute(5)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 5)

    def test_load_a_index_indirect_x(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xA1
        self.cpu.memory.data[0xFFFD] = 0x20
        self.cpu.x = 0x04
        self.cpu.memory.data[0x0024] = 0x80
        self.cpu.memory.data[0x0025] = 0x25
        self.cpu.memory.data[0x2580] = 0x42

        self.cpu.execute(6)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 6)

    def test_load_a_indirect_index_y(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xB1
        self.cpu.memory.data[0xFFFD] = 0x20
        self.cpu.memory.data[0x0020] = 0x30
        self.cpu.memory.data[0x0021] = 0x40
        self.cpu.y = 0x04
        self.cpu.memory.data[0x4034] = 0x42

        self.cpu.execute(5)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 5)

    def test_load_a_indirect_index_y_page_boundary_crossed(self):
        self.cpu.reset()

        self.cpu.memory.data[0xFFFC] = 0xB1
        self.cpu.memory.data[0xFFFD] = 0x20
        self.cpu.memory.data[0x0020] = 0x02
        self.cpu.memory.data[0x0021] = 0x44
        self.cpu.y = 0xFF
        self.cpu.memory.data[0x4501] = 0x42

        self.cpu.execute(6)
        self.assertEquals(self.cpu.a, 0x42)
        self.assertEquals(self.cpu.taken_cycles, 6)
