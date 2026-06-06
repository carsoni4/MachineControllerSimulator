from machine_controller.controller import MachineController
from machine_controller.enums import BucketPosition, CommandAction, CommandStatus

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