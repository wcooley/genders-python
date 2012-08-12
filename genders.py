#!/usr/bin/env python26

import sys
if sys.version_info[0] < 3 and sys.version_info[1] < 5:
    raise NotImplementedError, 'This module requires Python 2.5 or later'

import ctypes
from ctypes import CDLL, c_char_p, pointer, byref
from ctypes.util import find_library
from ctypes import *

genders_library_file = find_library('genders')

if not genders_library_file:
    raise NotImplementedError, 'Unable to find genders library'

libgenders = CDLL(genders_library_file)

# Argument types
libgenders.genders_load_data.argtypes = [c_void_p, c_char_p]
libgenders.genders_isnode.argtypes = [c_void_p, c_char_p]
libgenders.genders_isattr.argtypes = [c_void_p, c_char_p]
libgenders.genders_isattrval.argtypes = [c_void_p, c_char_p]

# Non-int return types
libgenders.genders_handle_create.restype = c_void_p
libgenders.genders_strerror.restype = c_char_p
libgenders.genders_errormsg.restype = c_char_p

libgenders.genders_isattr.restype = c_bool
libgenders.genders_isnode.restype = c_bool
libgenders.genders_isattrval.restype = c_bool

libgenders.genders_perror.restype = None

# ctypes errcheck {{{
def errcheck(result, func, args):
    """ errcheck for functions that return less-than-zero on error """
    if result < 0:
        handle = args[0]
        errnum = libgenders.genders_errnum(handle)
        errmsg = libgenders.genders_errormsg(handle)
        errmsg += " from func " + func.__name__
        raise errnum_exceptions[errnum](errmsg)
    return args

# Circular dependency: We need a handle to process the error, so we deal with
# handle_create where we use it. Likewise for errnum, strerror, errmsg, perror.
libgenders.genders_handle_destroy.errcheck = errcheck
libgenders.genders_load_data.errcheck = errcheck
libgenders.genders_getnumnodes.errcheck = errcheck
libgenders.genders_getnumattrs.errcheck = errcheck
libgenders.genders_getmaxattrs.errcheck = errcheck
libgenders.genders_getmaxnodelen.errcheck = errcheck
libgenders.genders_getmaxattrlen.errcheck = errcheck
libgenders.genders_getmaxvallen.errcheck = errcheck
libgenders.genders_nodelist_create.errcheck = errcheck
libgenders.genders_nodelist_clear.errcheck = errcheck
libgenders.genders_nodelist_destroy.errcheck = errcheck
libgenders.genders_attrlist_create.errcheck = errcheck
libgenders.genders_attrlist_clear.errcheck = errcheck
libgenders.genders_attrlist_destroy.errcheck = errcheck
libgenders.genders_vallist_create.errcheck = errcheck
libgenders.genders_vallist_clear.errcheck = errcheck
libgenders.genders_vallist_destroy.errcheck = errcheck
libgenders.genders_getnodename.errcheck = errcheck
libgenders.genders_getnodes.errcheck = errcheck
libgenders.genders_getattr.errcheck = errcheck
libgenders.genders_getattr_all.errcheck = errcheck
libgenders.genders_testattr.errcheck = errcheck
libgenders.genders_testattrval.errcheck = errcheck
libgenders.genders_isnode.errcheck = errcheck
libgenders.genders_isattr.errcheck = errcheck
libgenders.genders_isattrval.errcheck = errcheck
libgenders.genders_index_attrvals.errcheck = errcheck
libgenders.genders_query.errcheck = errcheck
libgenders.genders_testquery.errcheck = errcheck
libgenders.genders_parse.errcheck = errcheck

def errcheck_null(result, func, args):
    if not result:
        raise Exception("Error allocating memory in " + func.__name__ )
    return args

libgenders.genders_handle_create.errcheck = errcheck_null

# }}} errcheck

# Exceptions {{{
errnum_exceptions = [None]

# These are ordered so that each index corresponds with the errnum
class ErrNullHandle(Exception): pass
errnum_exceptions.append(ErrNullHandle)

class ErrOpen(Exception): pass
errnum_exceptions.append(ErrOpen)

class ErrRead(Exception): pass
errnum_exceptions.append(ErrRead)

class ErrParse(Exception): pass
errnum_exceptions.append(ErrParse)

class ErrNotLoaded(Exception): pass
errnum_exceptions.append(ErrNotLoaded)

class ErrIsLoaded(Exception): pass
errnum_exceptions.append(ErrIsLoaded)

class ErrOverflow(Exception): pass
errnum_exceptions.append(ErrOverflow)

class ErrParameters(Exception): pass
errnum_exceptions.append(ErrParameters)

class ErrNullPtr(Exception): pass
errnum_exceptions.append(ErrNullPtr)

class ErrNotFound(Exception): pass
errnum_exceptions.append(ErrNotFound)

class ErrOutMem(Exception): pass
errnum_exceptions.append(ErrOutMem)

class ErrSyntax(Exception): pass
errnum_exceptions.append(ErrSyntax)

class ErrMagic(Exception): pass
errnum_exceptions.append(ErrMagic)

class ErrInternal(Exception): pass
errnum_exceptions.append(ErrInternal)

class ErrNumrange(Exception): pass
errnum_exceptions.append(ErrNumrange)

# }}} End Exceptions

class Genders(object):
    def __init__(self, genders_file=None, no_auto=False):

        if not no_auto:
            self.handle_create()
            self.load_data(genders_file)

    def handle_create(self):
        self._handle = libgenders.genders_handle_create()


    def handle_destroy(self):
        libgenders.genders_handle_destroy(self._handle)

    def load_data(self, genders_file=None):
        libgenders.genders_load_data(self._handle, genders_file)

    def errnum(self):
        return libgenders.genders_errnum(self._handle)

    def strerror(self, err):
        return libgenders.genders_strerror(err)

    def errormsg(self):
        return libgenders.genders_errormsg(self._handle)

    def perror(self, msg=None):
        libgenders.genders_perror(self._handle, msg)

    def getnumnodes(self):
        return libgenders.genders_getnumnodes(self._handle)

    def getnumattrs(self):
        return libgenders.genders_getnumattrs(self._handle)

    def getmaxattrs(self):
        return libgenders.genders_getmaxattrs(self._handle)

    def getmaxnodelen(self):
        return libgenders.genders_getmaxnodelen(self._handle)

    def getmaxattrlen(self):
        return libgenders.genders_getmaxattrlen(self._handle)

    def getmaxvallen(self):
        return libgenders.genders_getmaxvallen(self._handle)

    def _list_create(self, create_func):
        clist = pointer(c_char_p(0))
        create_func(self._handle, byref(clist))
        return clist

    def nodelist_create(self):
        return self._list_create(libgenders.genders_nodelist_create)

    def nodelist_clear(self, node_list):
        libgenders.genders_nodelist_clear(self._handle, node_list)

    def nodelist_destroy(self, node_list):
        libgenders.genders_nodelist_destroy(self._handle, node_list)

    def attrlist_create(self):
        return self._list_create(libgenders.genders_attrlist_create)

    def attrlist_clear(self, attr_list):
        libgenders.genders_attrlist_clear(self._handle, attr_list)

    def attrlist_destroy(self, attr_list):
         libgenders.genders_attrlist_destroy(self._handle, attr_list)

    def vallist_create(self):
        return self._list_create(libgenders.genders_vallist_create)

    def vallist_clear(self, val_list):
        libgenders.genders_vallist_clear(self._handle, val_list)

    def vallist_destroy(self, val_list):
        libgenders.genders_vallist_destroy(self._handle, val_list)

    def getnodename(self):
        bufsz = self.getmaxnodelen()+1
        node = c_char_p(bufsz)
        libgenders.genders_getnodename(self._handle, node, bufsz)
        return node

    def getnodes(self, attr=None, val=None, node_list=None):
        if not node_list:
            node_list = self.nodelist_create()
            node_list_destroy = True
        else:
            node_list_destroy = False

        ret = libgenders.genders_getnodes(self._handle, node_list, self.getnumnodes(), attr, val)

        if ret < 0:
            raise errnum_exceptions[self.errnum()]()

        pylist = node_list[0:ret]
        if node_list_destroy:
            self.nodelist_destroy(node_list)
        return pylist

    # def getattr
    # def getattr_all
    # def testattr
    # def testattrval

    def isnode(self, node=None):
        return libgenders.genders_isnode(self._handle, node)

    def isattr(self, attr=None):
        return libgenders.genders_isattr(self._handle, attr)

    def isattrval(self, attr=None, val=None):
        return libgenders.genders_isattrval(self._handle, attr, val)

    # def index_attrvals

    def query(self, query_str):
        node_list = self.nodelist_create()
        query_ret = libgenders.genders_query(self._handle, node_list, self.getnumnodes(), query_str)

        pylist = node_list[0:query_ret]
        self.nodelist_destroy(node_list)
        return pylist

    # def testquery
    # def parse

# vim:fdm=marker
