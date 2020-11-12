import time
import typing

from helpers.logger import logger


def retry(success_condition: typing.Callable = lambda x: x is not None, max_attempts=0,
          exception_on_error: Exception = None, retry_sleep_time=1):
    def wrapper(func):
        name = func.__name__

        def wrapped_args(*args):
            for retry_count in range(max_attempts):
                result = func(*args)
                if success_condition(result):
                    return result

                logger.info(
                    "{}: retrying.. ({} retries remaining) Sleeping for 1 sec".format(name, max_attempts - retry_count))
                time.sleep(retry_sleep_time)

            logger.info("{}: end of retries".format(name))
            if exception_on_error is not None:
                raise exception_on_error
            return result

        return wrapped_args

    return wrapper


def retry_on_exception(max_attempts=0, exception_on_error: Exception = None, retry_sleep_time=1):
    def wrapper(func):
        name = func.__name__

        def wrapped_args(*args):
            last_ex = None
            for retry_count in range(max_attempts):
                try:
                    result = func(*args)
                    return result
                except Exception as ex:
                    logger.info("{}: retrying.. ({} retries remaining) Sleeping for 1 sec".format(name,
                                                                                                  max_attempts - retry_count))
                    time.sleep(retry_sleep_time)
                    last_ex = ex
            last_ex = last_ex or exception_on_error
            raise last_ex

        return wrapped_args

    return wrapper
