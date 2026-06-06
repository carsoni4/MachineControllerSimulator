from machine_controller.controller import MachineController
from machine_controller.enums import BucketPosition, CommandAction, CommandStatus
from machine_controller.constants import MAX_BUCKET_SPEED

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