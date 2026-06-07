from collections import deque
from .enums import CommandAction, CommandStatus, BucketPosition
from .models import CommandResponse
from .constants import MAX_BUCKET_SPEED, MAX_TEMP, LOG_FILE
from .logger import CommandLogger


class MachineController:
    def __init__(self):
        self.engine_running = False
        self.engine_speed = 0
        self.temperature = 0
        self.bucket_position = BucketPosition.BUCKET_UP
        self.warning = False
        self.warning_message = ""

        self.command_queue = deque()
        self.logger = CommandLogger(LOG_FILE)

        self.command_handler = {
            CommandAction.ENGINE_START: self._handle_engine_start,
            CommandAction.ENGINE_STOP: self._handle_engine_stop,
            CommandAction.ENGINE_SPEED_SET: self._handle_engine_speed_set,
            CommandAction.BUCKET_MOVE_UP: self._handle_bucket_move_up,
            CommandAction.BUCKET_MOVE_DOWN: self._handle_bucket_move_down,
            CommandAction.TEMP_SET: self._handle_set_temp,
        }

    def send_command(self, command: str):
        parts = command.split()
        if len(parts) == 0:
            empty_response = CommandResponse(CommandStatus.ERROR, "EMPTY COMMAND")
            self.logger.log(command, empty_response)
            return empty_response
        actionStr = parts[0]

        try:
            action = CommandAction(actionStr)
        except ValueError:
            unknown_response = CommandResponse(CommandStatus.ERROR, "UNKNOWN COMMAND")
            self.logger.log(command, unknown_response)
            return unknown_response

        handler = self.command_handler.get(action)

        response: CommandResponse = handler(parts)  # execute
        self.logger.log(command, response)  # log

        return response

    def queue_command(self, command: str) -> CommandResponse:
        if not command.strip():
            emptyResponse = CommandResponse(CommandStatus.ERROR, "EMPTY COMMAND")
            self.logger.log(command, emptyResponse)
            return emptyResponse
        self.command_queue.append(command)
        response = CommandResponse(
            CommandStatus.OK, f"COMMAND: {command} WAS ADDED TO QUEUE"
        )
        self.logger.log(command, response)
        return response

    def process_next_command(self) -> CommandResponse:
        if not self.command_queue:
            errorResponse = CommandResponse(CommandStatus.ERROR, "COMMAND QUEUE EMPTY")
            self.logger.log("process_next_command", errorResponse)
            return errorResponse
        command = self.command_queue.popleft()
        response = self.send_command(command)
        return response

    def process_all_commands(self) -> list[CommandResponse]:
        listOfResponses = []

        if not self.command_queue:
            errorResponse = CommandResponse(CommandStatus.ERROR, "COMMAND QUEUE EMPTY")
            self.logger.log("process_all_commands", errorResponse)
            return [errorResponse]

        while self.command_queue:
            listOfResponses.append(self.process_next_command())

        return listOfResponses

    def get_machine_status(self):
        return {
            "engine_running": self.engine_running,
            "speed": self.engine_speed,
            "temperature": self.temperature,
            "bucket_position": self.bucket_position.value,
            "warning": self.warning,
            "warning_message": self.warning_message,
        }

    def _move_bucket(self, position: BucketPosition):
        if self.engine_speed > MAX_BUCKET_SPEED:
            return CommandResponse(
                CommandStatus.ERROR,
                f"CAN NOT MOVE BUCKET AS CURRENT SPEED: {self.engine_speed} IS GREATER THAN MAX BUCKET SPEED: {MAX_BUCKET_SPEED}",
            )

        self.bucket_position = position
        return CommandResponse(
            CommandStatus.OK,
            f"BUCKET SUCCESFULLY SET TO POSITION: {self.bucket_position.value}",
        )

    def _handle_engine_start(self, parts):
        self.engine_running = True
        return CommandResponse(CommandStatus.OK, "ENGINE STARTED SUCCESFULLY")

    def _handle_engine_stop(self, parts):
        self.engine_speed = 0
        self.engine_running = False
        return CommandResponse(CommandStatus.OK, "ENGINE STOPPED SUCCESFULLY")

    def _handle_engine_speed_set(self, parts):
        if self.engine_running == False:
            return CommandResponse(
                CommandStatus.ERROR, "ENGINE NOT RUNNING, CANT SET SPEED"
            )

        try:
            engineSpeed = int(parts[1])
        except (IndexError, ValueError):
            return CommandResponse(
                CommandStatus.ERROR, "INVALID ARGUMENTS FOR ENGINE SPEED"
            )

        if engineSpeed < 0:
            return CommandResponse(
                CommandStatus.ERROR, "ENGINE SPEED CAN NOT BE NEGATIVE"
            )

        self.engine_speed = engineSpeed
        return CommandResponse(CommandStatus.OK, f"ENGINE SPEED SET TO {engineSpeed}")

    def _handle_bucket_move_up(self, parts):
        return self._move_bucket(BucketPosition.BUCKET_UP)

    def _handle_bucket_move_down(self, parts):
        return self._move_bucket(BucketPosition.BUCKET_DOWN)

    def _handle_set_temp(self, parts):
        try:
            temp = int(parts[1])
        except (IndexError, ValueError):
            return CommandResponse(
                CommandStatus.ERROR, "INVALID ARGUMENTS FOR TEMP_SET"
            )

        self.temperature = temp

        if self.temperature > MAX_TEMP:
            self.warning = True
            self.warning_message = f"{CommandAction.TEMP_SET.value} HIT MAX TEMP"

            return CommandResponse(
                CommandStatus.WARNING,
                f"TEMPERATURE WAS SET TO: {self.temperature} BUT IS GREATER THAN MAX RECOMMENDED TEMP: {MAX_TEMP}",
            )

        self.warning = False
        self.warning_message = ""

        return CommandResponse(
            CommandStatus.OK, f"TEMPERATURE SET TO: {temp} SUCCESFULLY"
        )
