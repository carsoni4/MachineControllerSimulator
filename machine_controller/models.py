from dataclasses import dataclass
from .enums import CommandStatus

@dataclass(frozen=True)
class CommandResponse:
    status: CommandStatus
    message: str