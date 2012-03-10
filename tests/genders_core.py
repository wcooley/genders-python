#!/usr/bin/env python26

from pprint import pprint as pp
import sys
import unittest

sys.path.insert(0, '.')
sys.path.insert(0, '..')

import genders

class TestGendersCore(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders()

    def test_handle_create(self):
        self.assertEqual(self.genders.handle_create(), None)

    def test_handle_destroy(self):
        self.genders.handle_create()
        self.assertEqual(self.genders.handle_destroy(), None)

class TestGendersLoad(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders()
        self.genders.handle_create()

    def test_load_data(self):
        self.assertEqual(self.genders.load_data("test-data/genders"), None)

#    def test_load_data_fail(self):
#        self.assertRaises(Exception("genders file parse error"), self.genders.load_data("test-data/genders.dup-attr"))

class TestGendersTests(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders()
        self.genders.handle_create()
        self.genders.load_data("test-data/genders")

    def test_isnode_true(self):
        self.assertTrue(self.genders.isnode("host1"))

    def test_isnode_false(self):
        self.assertFalse(self.genders.isnode("Xhost1"))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGendersCore)
    suite.addTest(loader.loadTestsFromTestCase(TestGendersLoad))
    suite.addTest(loader.loadTestsFromTestCase(TestGendersTests))

    unittest.TextTestRunner(verbosity=2).run(suite)

