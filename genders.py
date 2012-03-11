#!/usr/bin/env python26

#from ctypes import CDLL, c_char_p, pointer, byref
from ctypes import *

libgenders = CDLL("libgenders.so")

errnum_exceptions = [None]

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

class Genders(object):
    def __init__(self, genders_file=None):
        pass
#        self.handle_create()

#        if self.load_data(genders_file) != 0:
#            raise Exception(self.errormsg())

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
        self.node_list = POINTER(POINTER(POINTER(c_char)))
        #libgenders.genders_nodelist_create.
        libgenders.genders_nodelist_create(self._handle, self.node_list)

    def query(self, query_str):
        query_str = c_char_p(query_str)

        #nodes = byref(c_char_p * 500)
        #nodes = pointer(c_char_p * 500)
        #nodes = POINTER(c_char_p * 500)
        node_buf = (c_char_p * 500)()
        libgenders.genders_query.argtypes = [c_int, POINTER(c_char_p), c_int, c_char_p]
        query_ret = libgenders.genders_query(self._handle, cast(node_buf, POINTER(c_char_p)), 500, query_str)
        print "ret:", query_ret

        return node_buf
