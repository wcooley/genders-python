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
        self.node_list = pointer(pointer(pointer(c_char_p(1))))
        libgenders.genders_nodelist_create.argtypes = [c_void_p, POINTER(POINTER(POINTER(c_char_p)))]
        libgenders.genders_nodelist_create(self._handle, self.node_list)
        return self.node_list

    def query(self, query_str):
        charptr = POINTER(c_char)

        node_buf = (charptr * 500)()
        node_buf_ptr = pointer(node_buf)
        node_buf[0] = create_string_buffer(10)
        node_buf[1] = create_string_buffer(10)
        libgenders.genders_query.restype = c_int
        query_ret = libgenders.genders_query(self._handle, node_buf, 500, query_str)
        #print "ret:", query_ret

        if query_ret < 0:
            raise errnum_exceptions[self.errnum()]()

        node_list = []

        for node in node_buf:
            if node.contents.value == '\x00': break
            node = cast(node, c_char_p)
            node_list.append(node.value)

        return node_list
