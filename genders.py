#!/usr/bin/env python26

import ctypes
from ctypes import CDLL, c_char_p, pointer, byref
from ctypes.util import find_library
from ctypes import *

import sys

genders_library_file = find_library('genders')

if not genders_library_file:
    raise NotImplementedError, 'Unable to find genders library'

libgenders = CDLL(genders_library_file)

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

def _nodelist_to_list(node_list, length):
    """ Converts a Genders node_list to a native Python list """
    # FIXME Is there a way to do this with ctypes directly?
    return [ node_list[i] for i in xrange(length) ]

class Genders(object):
    def __init__(self, genders_file=None, no_auto=False):

        if not no_auto:
            self.handle_create()
            self.load_data(genders_file)

    def handle_create(self):
        self._handle = c_void_p(libgenders.genders_handle_create())

        if not self._handle:
            raise Exception("Error allocating memory")

    def handle_destroy(self):
        if libgenders.genders_handle_destroy(self._handle) != 0:
            raise errnum_exceptions[self.errnum()]()

    def load_data(self, genders_file=None):
        if libgenders.genders_load_data(self._handle, c_char_p(genders_file)) != 0:
            raise errnum_exceptions[self.errnum()]()

    def isnode(self, node=None):
        node = c_char_p(node)
        return bool(libgenders.genders_isnode(self._handle, node))

    def isattr(self, attr=None):
        attr = c_char_p(attr)
        return bool(libgenders.genders_isattr(self._handle, attr))

    def isattrval(self, attr=None, val=None):
        attr = c_char_p(attr)
        val = c_char_p(val)
        return bool(libgenders.genders_isattrval(self._handle, attr, val))

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

    def errnum(self):
        return libgenders.genders_errnum(self._handle)

    def strerror(self, err):
        libgenders.genders_strerror.restype = c_char_p
        return libgenders.genders_strerror(err)

    def errormsg(self):
        libgenders.genders_errormsg.restype = c_char_p
        return libgenders.genders_errormsg(self._handle)

    def perror(self, msg=None):
        libgenders.genders_perror(self._handle, msg)

    def nodelist_create(self):
        self.node_list = pointer(c_char_p(1))
        libgenders.genders_nodelist_create(self._handle, byref(self.node_list))

        return self.node_list

    def query(self, query_str):
        node_buf = self.nodelist_create()
        query_ret = libgenders.genders_query(self._handle, node_buf, self.getnumnodes(), query_str)

        if query_ret < 0:
            raise errnum_exceptions[self.errnum()]()

        return _nodelist_to_list(node_buf, query_ret)

