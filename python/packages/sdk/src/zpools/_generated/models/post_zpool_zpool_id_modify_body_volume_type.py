from enum import Enum


class PostZpoolZpoolIdModifyBodyVolumeType(str, Enum):
    GP3 = "gp3"
    IO1 = "io1"
    IO2 = "io2"

    def __str__(self) -> str:
        return str(self.value)
