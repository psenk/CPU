import unittest


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover('test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_tests()
