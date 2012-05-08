#-*- coding: utf-8 -*-
import unittest

if __name__ == '__main__':
    tests = unittest.defaultTestLoader.discover('test', 'test*.py')
    suite = unittest.TestSuite()
    suite.addTests(tests) 
    unittest.TextTestRunner(verbosity=2).run(suite)
