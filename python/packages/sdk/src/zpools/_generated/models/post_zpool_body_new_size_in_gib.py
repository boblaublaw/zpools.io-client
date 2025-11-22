from enum import IntEnum


class PostZpoolBodyNewSizeInGib(IntEnum):
    VALUE_125 = 125

    def __str__(self) -> str:
        return str(self.value)
