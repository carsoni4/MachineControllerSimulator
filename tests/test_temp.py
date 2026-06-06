from machine_controller.controller import MachineController
from machine_controller.enums import CommandAction, CommandStatus
from machine_controller.constants import MAX_TEMP

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