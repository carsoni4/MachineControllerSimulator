from machine_controller.controller import MachineController
from machine_controller.logger import CommandLogger
from machine_controller.enums import CommandAction, CommandStatus

TEST_LOG = "test.log"

def test_general_logging(tmp_path):
    temp_log = tmp_path / TEST_LOG
    controller = MachineController()

    #override logger with temp path instead of constant in constants.py
    controller.logger = CommandLogger(str(temp_log))

    #test sending valid command
    response = controller.send_command(CommandAction.ENGINE_START.value)

    assert response.status == CommandStatus.OK
    
    assert temp_log.exists()
    content = temp_log.read_text()
    
    assert "ENGINE_START" in content
    assert "STATUS: OK" in content

    #test sending invalid command
    response = controller.send_command("NOT_REAL_COMMAND")
    content = temp_log.read_text()
    assert "NOT_REAL_COMMAND" in content
    assert "STATUS: ERROR" in content

def test_queue_logging(tmp_path):
    temp_log = tmp_path / TEST_LOG
    controller = MachineController()

    #override logger with temp path instead of constant in constants.py
    controller.logger = CommandLogger(str(temp_log))

    response = controller.queue_command(CommandAction.ENGINE_START.value)
    
    assert response.status == CommandStatus.OK

    assert temp_log.exists()
    content = temp_log.read_text()
    
    assert "ENGINE_START" in content
    assert "STATUS: OK" in content
    assert "WAS ADDED TO QUEUE" in content

def test_failed_queue_logging(tmp_path):
    temp_log = tmp_path / TEST_LOG
    controller = MachineController()
    controller.logger = CommandLogger(str(temp_log))
    
    response = controller.queue_command("")
    assert response.status == CommandStatus.ERROR
    assert response.message == "EMPTY COMMAND"

    assert temp_log.exists()
    content = temp_log.read_text()

    assert "STATUS: ERROR" in content
    assert "EMPTY COMMAND" in content

    response = controller.process_next_command()

    assert response.status == CommandStatus.ERROR
    assert response.message == "COMMAND QUEUE EMPTY"
    
    content = temp_log.read_text()

    assert "process_next_command" in content
    assert "COMMAND QUEUE EMPTY" in content

    response = controller.process_all_commands()
    assert response[0].status == CommandStatus.ERROR
    assert response[0].message == "COMMAND QUEUE EMPTY"

    content = temp_log.read_text()

    assert "process_all_commands" in content
    assert "COMMAND QUEUE EMPTY" in content