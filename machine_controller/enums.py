from enum import Enum

class CommandStatus(Enum):
    OK = "OK"
    ERROR = "ERROR"
    WARNING = "WARNING"


class CommandAction(Enum):
    ENGINE_START = "ENGINE_START"
    ENGINE_STOP = "ENGINE_STOP"
    ENGINE_SPEED_SET = "ENGINE_SPEED_SET"
    BUCKET_MOVE_DOWN = "BUCKET_MOVE_DOWN"
    BUCKET_MOVE_UP = "BUCKET_MOVE_UP"
    TEMP_SET = "TEMP_SET"


class BucketPosition(Enum):
    BUCKET_DOWN = "BUCKET_DOWN"
    BUCKET_UP = "BUCKET_UP"