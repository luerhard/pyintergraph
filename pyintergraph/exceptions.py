# noqa: D107
"""Collection of all custom exceptions that can be thrown in this package."""


class PyIntergraphInferError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PyIntergraphCompatibilityError(Exception):
    pass
