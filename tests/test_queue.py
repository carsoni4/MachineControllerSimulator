from machine_controller.controller import MachineController
from machine_controller.enums import BucketPosition, CommandAction, CommandStatus

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