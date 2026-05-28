from enum import Enum

MAX_BUCKET_SPEED = 10
MAX_TEMP = 100

class MachineController:
    def __init__(self):
         self.engine_running = False
         self.engine_speed = 0
         self.temperature = 70
         self.bucket_position = BucketPosition.BUCKET_UP
         self.warning = False
         self.warning_message = ""

    def get_machine_status(self):
        return {  
          "engine_running": self.engine_running,
          "speed": self.engine_speed,
          "temperature": self.temperature,
          "bucket_position": self.bucket_position,
          "warning": self.warning,
          "warning_message": self.warning_message
        }


    def send_command(self, command: str):
         parts = command.split()
         action = parts[0]

         if action == CommandAction.ENGINE_START.value:
              self.engine_running = True
              return CommandResponse(CommandStatus.OK, "ENGINE STARTED SUCCESFULLY")
         
         if action == CommandAction.ENGINE_STOP.value:
             self.engine_running = False
             return CommandResponse(CommandStatus.OK, "ENGINE STOPPED SUCCESFULLY")
         
         if action == CommandAction.ENGINE_SPEED_SET.value:
              if self.engine_running == False:
                  return CommandResponse(CommandStatus.ERROR, "ENGINE NOT RUNNING, CANT SET SPEED")
              
              engineSpeed = int(parts[1])
              if(engineSpeed < 0):
                  return CommandResponse(CommandStatus.ERROR, "ENGINE SPEED CAN NOT BE NEGATIVE")
              
              self.engine_speed = engineSpeed
              return CommandResponse(CommandStatus.OK, f"ENGINE SPEED SET TO {engineSpeed}") 

         if action == CommandAction.BUCKET_MOVE_DOWN.value:
              if self.engine_speed > MAX_BUCKET_SPEED:
                   return CommandResponse(CommandStatus.ERROR, f"CAN NOT MOVE BUCKET AS CURRENT SPEED: {self.engine_speed} IS GREATER THAN MAX BUCKET SPEED: {MAX_BUCKET_SPEED}")
              else:
                   self.bucket_position = BucketPosition.BUCKET_DOWN
                   return CommandResponse(CommandStatus.OK, f"BUCKET SUCCESFULLY SET TO POSITION: {self.bucket_position}")
          
         if action == CommandAction.BUCKET_MOVE_UP.value:
              if self.engine_speed > MAX_BUCKET_SPEED:
                   return CommandResponse(CommandStatus.ERROR, f"CAN NOT MOVE BUCKET AS CURRENT SPEED: {self.engine_speed} IS GREATER THAN MAX BUCKET SPEED: {MAX_BUCKET_SPEED}")
              else:
                   self.bucket_position = BucketPosition.BUCKET_UP
                   return CommandResponse(CommandStatus.OK, f"BUCKET SUCCESFULLY SET TO POSITION: {self.bucket_position}") 
          
         if action == CommandAction.TEMP_SET.value:
              temp = int(parts[1])
              self.temperature = temp

              if self.temperature > MAX_TEMP:
                  self.warning = True
                  self.warning_message = f"{CommandAction.TEMP_SET} HIT MAX TEMP"
                  return CommandResponse(CommandStatus.WARNING, f"TEMPERATURE: {self.temperature} IS GREATER THAN MAX RECOMMENDED TEMP: {MAX_TEMP}")
              return CommandResponse(CommandStatus.OK, f"TEMPERATURE SET TO: {temp} SUCCESFULLY") 
         
         # No Command Was Hit
         return CommandResponse(CommandStatus.ERROR, "UNKNOWN COMMAND")
    
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

class CommandResponse:
     def __init__(self, status, message):
          self.status = status
          self.message = message
