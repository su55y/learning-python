class Mod3Class:
    msg = ""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self) -> str:
        return f"from {__name__}.{Mod3Class.__name__}({self.__dict__})"
