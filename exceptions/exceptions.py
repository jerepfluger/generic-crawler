class MalformedHtmlException(Exception):
    pass


class ProxyException(Exception):
    def __init__(self, name, message, proxy):
        self.name = name
        self.message = message
        self.proxy = proxy


class BannedProxyException(ProxyException):
    def __init__(self, proxy):
        super(ProxyException, self).__init__("BannedProxyException", "IP is currently banned", proxy)
        self.name = "BannedProxyException"
        self.message = "IP is currently banned"
        self.proxy = proxy


class ConnectionRefusedException(ProxyException):
    def __init__(self, proxy):
        super(ProxyException, self).__init__("ConnectionRefusedException", "Connection refused", proxy)
        self.name = "ConnectionRefusedException"
        self.message = "Connection refused"
        self.proxy = proxy


class TimeoutProxyException(ProxyException):
    def __init__(self, proxy):
        super(ProxyException, self).__init__("TimeoutProxyException", "Timeout given proxy is too slow to load webpage", proxy)
        self.name = "TimeoutProxyException"
        self.message = "Timeout given proxy is too slow to load webpage"
        self.proxy = proxy


class NonExistentCombinationsException(Exception):
    def __init__(self, message):
        self.message = message
