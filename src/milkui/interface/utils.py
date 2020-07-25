import socket
import rubicon.objc as objc
from contextlib import closing
from threading import Semaphore
from PyObjCTools import AppHelper

class _CallAfter:
    def __init__(self):
        self._semaphore = Semaphore(0)
        self._return_value = None

    def call(self, func, *args, **kwargs):
        def _run(func, *args, **kwargs):
            self._return_value = func(*args, **kwargs)
            self._semaphore.release()

        AppHelper.callAfter(_run, func, *args, **kwargs)
        self._semaphore.acquire()
        # convert nsobj to pyobj
        return objc.api.py_from_ns(self._return_value)

# this function fix not main thread running error 
call_after = lambda func, *args, **kwargs: _CallAfter().call(func, *args, **kwargs)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]