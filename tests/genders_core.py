#!/usr/bin/env python26

from pprint import pprint as pp
import sys
import unittest

sys.path.insert(0, '.')
sys.path.insert(0, '..')

import genders

class TestGendersCore(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders(no_auto=True)

    def test_handle_create(self):
        self.assertEqual(self.genders.handle_create(), None)

    def test_handle_destroy(self):
        self.genders.handle_create()
        self.assertEqual(self.genders.handle_destroy(), None)

class TestGendersLoad(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders(no_auto=True)
        self.genders.handle_create()

    def test_load_data(self):
        self.assertEqual(self.genders.load_data("test-data/genders"), None)

    def test_load_data_fail(self):
        self.assertRaises(genders.ErrParse, self.genders.load_data,
                "test-data/genders.dup-attr")

class TestGendersPredicates(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    def test_isnode_true(self):
        self.assertTrue(self.genders.isnode("host1"))

    def test_isnode_false(self):
        self.assertFalse(self.genders.isnode("Xhost1"))

    def test_isattr_true(self):
        self.assertTrue(self.genders.isattr("testhost"))

    def test_isattr_false(self):
        self.assertFalse(self.genders.isattr("Xtesthost"))

    def test_isattrval_true(self):
        self.assertTrue(self.genders.isattrval("os", "rhel5"))

    def test_isattrval_false(self):
        self.assertFalse(self.genders.isattrval("Xos", "rhel5"))
        self.assertFalse(self.genders.isattrval("os", "Xrhel5"))

#class TestGendersGetNums(unittest.TestCase):
#
#    def setUp(self):
#        self.genders = genders.Genders()
#        self.genders.handle_create()
#        self.genders.load_data("test-data/genders")
#
#    def test_getnumnodes(self):
#        self.assertEqual(self.genders.getnumnodes(), 1)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGendersCore)
    suite.addTest(loader.loadTestsFromTestCase(TestGendersLoad))
    suite.addTest(loader.loadTestsFromTestCase(TestGendersPredicates))

    unittest.TextTestRunner(verbosity=2).run(suite)

