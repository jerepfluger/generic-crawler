import time

from helpers import logger as log


def measure_time(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        log.logger.info('%r (%r, %r) took %2.2f seconds' % (method.__name__, args, kw, te - ts))
        return result

    return timed
