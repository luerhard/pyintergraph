from contextlib import contextmanager
import sys

@contextmanager
def preserve_dlopenflags(flags):
    """A context manager that temporarily sets the dlopen flags and then returns them to previous values.
    """
    outer_flags = sys.getdlopenflags()
    try:
        sys.setdlopenflags(flags)
        yield
    finally:
        sys.setdlopenflags(outer_flags)


@contextmanager
def boost_python_dlopen_flags():
    """A context manager that temporarily sets the dlopen flags for loading multiple
    boost.python modules and then returns them to previous values.
    """
    flags = None
    try:
        import DLFCN
        flags = DLFCN.RTLD_NOW | DLFCN.RTLD_GLOBAL
    except:
        import os
        flags = os.RTLD_NOW | os.RTLD_GLOBAL
    if None != flags:
        with preserve_dlopenflags(flags):
            yield
    else:
        yield
