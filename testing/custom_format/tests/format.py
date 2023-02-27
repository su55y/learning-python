import enum
import unittest


class ResultFormat(unittest.TextTestResult):
    class MsgType(enum.Enum):
        ERROR = enum.auto()
        FAIL = enum.auto()
        PASS = enum.auto()

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.verbosity = verbosity

    def _method_fmt(self, name: str) -> str:
        return f"\x1b[1;1m{name}\x1b[0m"

    def _msg_fmt(self, type: MsgType, method: str, err=None) -> str:
        prefix = "[\x1b[32;1mPASS\x1b[0m]"
        match type:
            case self.MsgType.FAIL:
                prefix = "[\x1b[31;1mFAIL\x1b[0m]"
            case self.MsgType.ERROR:
                prefix = "[\x1b[31;1;4mERROR\x1b[0m]"

        return "{prefix} {method} {err}\n".format(
            prefix=prefix,
            method=self._method_fmt(method),
            err=(f"({err})" if err else ""),
        )

    def addSuccess(self, test):
        self.stream.write(self._msg_fmt(self.MsgType.PASS, test._testMethodName))

    def addFailure(self, test, err):
        super(unittest.TextTestResult, self).addFailure(test, err)
        self.stream.write(
            self._msg_fmt(
                self.MsgType.FAIL,
                test._testMethodName,
                err[1] or None,
            )
        )

    def addError(self, test, err):
        self.stream.write(
            self._msg_fmt(
                self.MsgType.ERROR,
                test._testMethodName,
                err[1] or None,
            )
        ) if self.verbosity == 1 else super().addError(test, err)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.stream.flush()
