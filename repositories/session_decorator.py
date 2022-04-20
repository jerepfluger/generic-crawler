def close_session(method):
    def session(*args, **kw):
        result = method(*args, **kw)
        result.close_session()

        return result
    return session
