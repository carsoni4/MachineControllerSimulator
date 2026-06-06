from machine_controller.controller import MachineController
from machine_controller.enums import BucketPosition, CommandAction, CommandStatus
from machine_controller.constants import MAX_BUCKET_SPEED, MAX_TEMP

def test_queue_command():
    controller = MachineController()
    response = controller.queue_command(CommandAction.ENGINE_START.value)
    
    assert response.status == CommandStatus.OK
    assert response.message == f"COMMAND: {CommandAction.ENGINE_START.value} WAS ADDED TO QUEUE"
    assert controller.engine_running == False

def test_empty_queue_command():
    controller = MachineController()
    response = controller.queue_command("")
    assert response.status == CommandStatus.ERROR
    assert response.message == "EMPTY COMMAND"

def test_empty_queue_process():
    controller = MachineController()
    response = controller.process_next_command()
    assert response.status == CommandStatus.ERROR
    assert response.message == "COMMAND QUEUE EMPTY"

def test_empty_queue_process_all():
    controller = MachineController()
    response = controller.process_all_commands()
    assert response[0].status == CommandStatus.ERROR
    assert response[0].message == "COMMAND QUEUE EMPTY"

def test_process_next_command():
    controller = MachineController()
    add_response = controller.queue_command(CommandAction.ENGINE_START.value)
    assert add_response.status == CommandStatus.OK
    assert add_response.message == f"COMMAND: {CommandAction.ENGINE_START.value} WAS ADDED TO QUEUE"
    assert controller.engine_running == False

    execute_response = controller.process_next_command()
    assert execute_response.status == CommandStatus.OK
    assert execute_response.message == "ENGINE STARTED SUCCESFULLY"
    assert controller.engine_running == True

def test_process_all_commands():
    controller = MachineController()
    #add two commands to queue
    add_response = controller.queue_command(CommandAction.ENGINE_START.value)
    assert add_response.status == CommandStatus.OK
    assert add_response.message == f"COMMAND: {CommandAction.ENGINE_START.value} WAS ADDED TO QUEUE"
    assert controller.engine_running == False

    second_add_response = controller.queue_command(CommandAction.ENGINE_STOP.value)
    assert second_add_response.status == CommandStatus.OK
    assert second_add_response.message == f"COMMAND: {CommandAction.ENGINE_STOP.value} WAS ADDED TO QUEUE"
    assert controller.engine_running == False
    

    #execute both commands, ensure correct num results
    execute_response = controller.process_all_commands()
    assert len(execute_response) == 2
    
    first_processed_response = execute_response[0] 
    second_processed_response = execute_response[1]

    assert first_processed_response.status == CommandStatus.OK
    assert first_processed_response.message == "ENGINE STARTED SUCCESFULLY"

    assert second_processed_response.status == CommandStatus.OK
    assert second_processed_response.message == "ENGINE STOPPED SUCCESFULLY"

    assert controller.engine_running == False

def test_engine_starts():
    controller = MachineController()

    response = controller.send_command(CommandAction.ENGINE_START.value)

    assert response.status == CommandStatus.OK
    assert response.message == "ENGINE STARTED SUCCESFULLY"
    assert controller.engine_running is True

def test_engine_stops():
    controller = MachineController()
    
    controller.send_command(CommandAction.ENGINE_START.value)
    response = controller.send_command(CommandAction.ENGINE_STOP.value)

    assert response.status == CommandStatus.OK
    assert response.message == "ENGINE STOPPED SUCCESFULLY"
    assert controller.engine_running is False

def test_engine_set_speed_invalid_args():
    controller = MachineController()
    controller.send_command(CommandAction.ENGINE_START.value)

    speed_before = controller.engine_speed

    response = controller.send_command(CommandAction.ENGINE_SPEED_SET.value)
    assert response.status == CommandStatus.ERROR
    assert response.message == "INVALID ARGUMENTS FOR ENGINE SPEED"
    assert controller.engine_speed == speed_before

def test_engine_set_speed_engine_running():
    controller = MachineController()

    speed = 10

    controller.send_command(CommandAction.ENGINE_START.value)
    response = controller.send_command(f"{CommandAction.ENGINE_SPEED_SET.value} {speed}")

    assert response.status == CommandStatus.OK
    assert response.message == f"ENGINE SPEED SET TO {speed}"
    assert controller.engine_speed == speed

def test_engine_set_speed_negative():
    controller = MachineController()

    speed = -1
    
    controller.send_command(CommandAction.ENGINE_START.value)
    response = controller.send_command(f"{CommandAction.ENGINE_SPEED_SET.value} {speed}")

    assert response.status == CommandStatus.ERROR
    assert response.message == f"ENGINE SPEED CAN NOT BE NEGATIVE"
    assert controller.engine_speed == 0

def test_engine_set_speed_engine_off():
    controller = MachineController()

    speed = 10

    response = controller.send_command(f"{CommandAction.ENGINE_SPEED_SET.value} {speed}")

    assert response.status == CommandStatus.ERROR
    assert response.message == "ENGINE NOT RUNNING, CANT SET SPEED"
    assert controller.engine_speed == 0

def test_bucket_move_down_success():
    controller = MachineController()

    response = controller.send_command(CommandAction.BUCKET_MOVE_DOWN.value)

    assert response.status == CommandStatus.OK
    assert response.message == f"BUCKET SUCCESFULLY SET TO POSITION: {BucketPosition.BUCKET_DOWN.value}"
    assert controller.bucket_position == BucketPosition.BUCKET_DOWN

def test_bucket_move_down_speed_fail():
    controller = MachineController()
    speed = 100

    controller.send_command(CommandAction.ENGINE_START.value)

    controller.send_command(f"{CommandAction.ENGINE_SPEED_SET.value} {speed}")

    assert controller.engine_speed == speed

    response = controller.send_command(f"{CommandAction.BUCKET_MOVE_DOWN.value}")

    assert response.status == CommandStatus.ERROR
    assert response.message == f"CAN NOT MOVE BUCKET AS CURRENT SPEED: {controller.engine_speed} IS GREATER THAN MAX BUCKET SPEED: {MAX_BUCKET_SPEED}"
    assert controller.bucket_position == BucketPosition.BUCKET_UP

def test_bucket_move_up_sucess():
    controller = MachineController()

    controller.send_command(CommandAction.BUCKET_MOVE_DOWN.value)

    assert controller.bucket_position == BucketPosition.BUCKET_DOWN

    response = controller.send_command(CommandAction.BUCKET_MOVE_UP.value)

    assert response.status == CommandStatus.OK
    assert response.message == f"BUCKET SUCCESFULLY SET TO POSITION: {BucketPosition.BUCKET_UP.value}"
    assert controller.bucket_position == BucketPosition.BUCKET_UP

def test_bucket_move_up_speed_fail():
    controller = MachineController()

    speed = 100

    controller.send_command(CommandAction.ENGINE_START.value)

    controller.send_command(CommandAction.BUCKET_MOVE_DOWN.value)
    
    assert controller.bucket_position == BucketPosition.BUCKET_DOWN

    controller.send_command(f"{CommandAction.ENGINE_SPEED_SET.value} {speed}")

    assert controller.engine_speed == 100

    response = controller.send_command(CommandAction.BUCKET_MOVE_UP.value)

    assert response.status == CommandStatus.ERROR
    assert response.message == f"CAN NOT MOVE BUCKET AS CURRENT SPEED: {controller.engine_speed} IS GREATER THAN MAX BUCKET SPEED: {MAX_BUCKET_SPEED}"
    assert controller.bucket_position == BucketPosition.BUCKET_DOWN

def test_temp_invalid_error():
    controller = MachineController()
    temperature_before = controller.temperature

    response = controller.send_command(CommandAction.TEMP_SET.value)

    assert response.status == CommandStatus.ERROR
    assert response.message == "INVALID ARGUMENTS FOR TEMP_SET"
    assert controller.temperature == temperature_before

def test_temp_warning_clear():
    controller = MachineController()
    high_temp = MAX_TEMP + 1
    normal_temp = 19

    high_response = controller.send_command(f"{CommandAction.TEMP_SET.value} {high_temp}")
    assert high_response.status == CommandStatus.WARNING
    assert high_response.message == f"TEMPERATURE WAS SET TO: {high_temp} BUT IS GREATER THAN MAX RECOMMENDED TEMP: {MAX_TEMP}"
    assert controller.temperature == high_temp

    assert controller.warning == True
    assert controller.warning_message == f"{CommandAction.TEMP_SET.value} HIT MAX TEMP"

    normal_response = controller.send_command(f"{CommandAction.TEMP_SET.value} {normal_temp}")
    assert normal_response.status == CommandStatus.OK
    assert normal_response.message == f"TEMPERATURE SET TO: {normal_temp} SUCCESFULLY"
    assert controller.temperature == normal_temp 

    assert controller.warning == False
    assert controller.warning_message == ""


def test_temp_set_success():
    controller = MachineController()

    temp = 10

    response = controller.send_command(f"{CommandAction.TEMP_SET.value} {temp}")

    assert response.status == CommandStatus.OK
    assert response.message == f"TEMPERATURE SET TO: {temp} SUCCESFULLY"
    assert controller.temperature == temp

def test_temp_set_at_max():
    controller = MachineController()

    temp = MAX_TEMP
    response = controller.send_command(f"{CommandAction.TEMP_SET.value} {temp}")

    assert response.status == CommandStatus.OK
    assert response.message == f"TEMPERATURE SET TO: {temp} SUCCESFULLY"
    assert controller.temperature == temp
    assert controller.warning == False
    assert controller.warning_message == ""

def test_temp_set_over_max():
    controller = MachineController()

    temp = MAX_TEMP + 1

    response = controller.send_command(f"{CommandAction.TEMP_SET.value} {temp}")

    assert response.status == CommandStatus.WARNING
    assert response.message == f"TEMPERATURE WAS SET TO: {controller.temperature} BUT IS GREATER THAN MAX RECOMMENDED TEMP: {MAX_TEMP}"
    assert controller.temperature == temp

def test_no_command_error():
    controller = MachineController()

    response = controller.send_command("THISISAFAKECOMMAND")

    assert response.status == CommandStatus.ERROR
    assert response.message == "UNKNOWN COMMAND"

def test_empty_command_error():
    controller = MachineController()
    response = controller.send_command("")

    assert response.status == CommandStatus.ERROR
    assert response.message == "EMPTY COMMAND"

def test_get_machine_status():
          controller = MachineController()

          response = controller.get_machine_status()
          
          assert response == {
          "engine_running": controller.engine_running,
          "speed": controller.engine_speed,
          "temperature": controller.temperature,
          "bucket_position": controller.bucket_position.value,
          "warning": controller.warning,
          "warning_message": controller.warning_message
          }