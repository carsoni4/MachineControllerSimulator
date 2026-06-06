from machine_controller.controller import MachineController
from machine_controller.enums import CommandStatus

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