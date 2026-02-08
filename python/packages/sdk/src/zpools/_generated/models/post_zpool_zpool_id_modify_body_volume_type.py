from enum import Enum


class PostZpoolZpoolIdModifyBodyVolumeType(str, Enum):
    GP3 = "gp3"
    SC1 = "sc1"

    def __str__(self) -> str:
        return str(self.value)
