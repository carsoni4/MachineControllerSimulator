from controller import MachineController
from controller import CommandAction
from controller import CommandStatus
from controller import BucketPosition
from controller import MAX_BUCKET_SPEED
from controller import MAX_TEMP

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
    assert response.message == f"BUCKET SUCCESFULLY SET TO POSITION: {BucketPosition.BUCKET_DOWN}"
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
    assert response.message == f"BUCKET SUCCESFULLY SET TO POSITION: {BucketPosition.BUCKET_UP}"
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

def test_temp_set_success():
    controller = MachineController()

    temp = 10

    response = controller.send_command(f"{CommandAction.TEMP_SET.value} {temp}")

    assert response.status == CommandStatus.OK
    assert response.message == f"TEMPERATURE SET TO: {temp} SUCCESFULLY"
    assert controller.temperature == temp

def test_temp_set_over_max():
    controller = MachineController()

    temp = MAX_TEMP + 1

    response = controller.send_command(f"{CommandAction.TEMP_SET.value} {temp}")

    assert response.status == CommandStatus.WARNING
    assert response.message == f"TEMPERATURE: {controller.temperature} IS GREATER THAN MAX RECOMMENDED TEMP: {MAX_TEMP}"
    assert controller.temperature == temp

def test_no_command_error():
    controller = MachineController()

    response = controller.send_command("THISISAFAKECOMMAND")

    assert response.status == CommandStatus.ERROR
    assert response.message == "UNKNOWN COMMAND"

def test_get_machine_status():
          controller = MachineController()

          response = controller.get_machine_status()
          
          assert response == {
          "engine_running": controller.engine_running,
          "speed": controller.engine_speed,
          "temperature": controller.temperature,
          "bucket_position": controller.bucket_position,
          "warning": controller.warning,
          "warning_message": controller.warning_message
          }