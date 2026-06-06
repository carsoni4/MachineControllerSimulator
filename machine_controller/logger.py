from datetime import datetime
from .models import CommandResponse

class CommandLogger:
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def log(self, command: str, response: CommandResponse):
        log_entry = (
            f"{datetime.now().isoformat()} | "  # iso to prevent timezone issues
            f"COMMAND: {command} | "
            f"STATUS: {response.status.value} | "
            f"MESSAGE: {response.message}\n"
        )

        with open(self.log_file, "a") as file:
            file.write(log_entry)