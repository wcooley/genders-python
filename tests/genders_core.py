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

    def test_load_data_err_parse(self):
        self.assertRaises(genders.ErrParse, self.genders.load_data,
                "test-data/genders.dup-attr")

    def test_load_data_err_open(self):
        self.assertRaises(genders.ErrOpen, self.genders.load_data,
                'test-data/does-not-exist')

    def test_load_data_err_isloaded(self):
        self.assertEqual(self.genders.load_data('test-data/genders'), None)
        self.assertRaises(genders.ErrIsLoaded, self.genders.load_data,
                'test-data/genders')

class TestGendersPredicates(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    # isnode
    def test_isnode_bool(self):
        self.assertEqual(type(self.genders.isnode('host1')), bool)
        self.assertEqual(type(self.genders.isnode('Xhost1')), bool)

    def test_isnode_true(self):
        self.assertTrue(self.genders.isnode("host1"))

    def test_isnode_false(self):
        self.assertFalse(self.genders.isnode("Xhost1"))

    # isattr
    def test_isattr_bool(self):
        self.assertEqual(type(self.genders.isattr('testhost')), bool)
        self.assertEqual(type(self.genders.isattr('testhostX')), bool)

    def test_isattr_true(self):
        self.assertTrue(self.genders.isattr("testhost"))

    def test_isattr_false(self):
        self.assertFalse(self.genders.isattr("Xtesthost"))

    # isattrval
    def test_isattrval_bool(self):
        self.assertEqual(type(self.genders.isattrval('os', 'rhel5')), bool)
        self.assertEqual(type(self.genders.isattrval('Xos', 'rhel5')), bool)

    def test_isattrval_true(self):
        self.assertTrue(self.genders.isattrval("os", "rhel5"))

    def test_isattrval_false(self):
        self.assertFalse(self.genders.isattrval("Xos", "rhel5"))
        self.assertFalse(self.genders.isattrval("os", "Xrhel5"))

class TestGendersGetNums(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    def test_getnumnodes(self):
        self.assertEqual(self.genders.getnumnodes(), 2)

    def test_getnumattrs(self):
        self.assertEqual(self.genders.getnumattrs(), 3)

    def test_getmaxattrs(self):
        self.assertEqual(self.genders.getmaxattrs(), 2)

    def test_getmaxnodelen(self):
        self.assertEqual(self.genders.getmaxnodelen(), 5)

    def test_getmaxattrlen(self):
        self.assertEqual(self.genders.getmaxattrlen(), 9)

    def test_getmaxvallen(self):
        self.assertEqual(self.genders.getmaxvallen(), 5)

class TestGendersQuery(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    def test_query(self):
        results = self.genders.query("os=rhel5")
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ['host1', 'host2'])

    def test_query2(self):
        results = self.genders.query('testhost2')
        self.assertEqual(len(results), 1)
        self.assertEqual(results, ['host2'])

class TestGendersGetNodes(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    def test_getnodes_all(self):
        results = self.genders.getnodes()
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ['host1', 'host2'])

    def test_getnodes_attr(self):
        results = self.genders.getnodes('os')
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ['host1', 'host2'])

    def test_getnodes_attrval(self):
        results = self.genders.getnodes('os', 'rhel5')
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ['host1', 'host2'])

class TestGendersLists(unittest.TestCase):

    def setUp(self):
        self.genders = genders.Genders("test-data/genders")

    def test_nodelist_create(self):
        r = self.genders.nodelist_create()
        self.assertNotEqual(r, 0)

    def test_nodelist_destroy(self):
        nl = self.genders.nodelist_create()
        self.genders.nodelist_destroy(nl)

    def test_nodelist_clear(self):
        nl = self.genders.nodelist_create()
        nodes = self.genders.getnodes('os', 'rhel5', nl)
        nodeslen = len(nodes)
        self.assertEqual(nodes, nl[0:nodeslen])
        self.genders.nodelist_clear(nl)
        # FIXME Is this really a good test?
        self.assertEqual(nl[0], '')

if __name__ == '__main__':
    import __main__

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTest(loader.loadTestsFromModule(__main__))

    unittest.TextTestRunner(verbosity=2).run(suite)

