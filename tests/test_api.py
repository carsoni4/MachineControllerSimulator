from fastapi.testclient import TestClient
from machine_controller.api import app
from machine_controller import api

STATUS_CODE_OK = 200
STATUS_CODE_ERROR_NOBODY = 422

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == STATUS_CODE_OK
    assert response.json() == {
        "message" : "Hi from Carson! Machine Controller API is running!"
    }

def test_status_endpoint():
    response = client.get("/status")

    assert response.status_code == STATUS_CODE_OK

    data = response.json()

    assert data["engine_running"] is False
    assert data["speed"] == 0
    assert data["temperature"] == 0
    assert data["bucket_position"] == "BUCKET_UP"
    assert data["warning"] is False
    assert data["warning_message"] == ""

def test_send_command():
    response = client.post("/commands/send", json={"command" : "ENGINE_START"})

    assert response.status_code == STATUS_CODE_OK
    
    data = response.json()

    assert data["status"] == "OK"
    assert data["message"] == "ENGINE STARTED SUCCESFULLY"

def test_send_unknown_command():
    response = client.post("/commands/send", json={"command" : "NOT_A_REAL_COMMAND"})

    assert response.status_code == STATUS_CODE_OK
    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "UNKNOWN COMMAND"

def test_send_empty_command():
    response = client.post("/commands/send", json={"command" : ""})

    assert response.status_code == STATUS_CODE_OK
    data = response.json()
    
    assert data["status"] == "ERROR"
    assert data["message"] == "EMPTY COMMAND"

def test_queue_command():
    response = client.post("/commands/queue", json={"command" : "ENGINE_START"})

    assert response.status_code == STATUS_CODE_OK

    data = response.json()

    assert data["status"] == "OK"
    assert data["message"] == "COMMAND: ENGINE_START WAS ADDED TO QUEUE"

def test_process_next_command():
    client.post("/commands/queue", json={"command" : "ENGINE_START"})
    response = client.post("/commands/process_next")

    assert response.status_code == STATUS_CODE_OK

    data = response.json()
    assert data["status"] == "OK"
    assert data["message"] == "ENGINE STARTED SUCCESFULLY"

def test_process_all_commands():
    api.controller.command_queue.clear()

    client.post("/commands/queue", json={"command": "ENGINE_START"})

    client.post("/commands/queue", json={"command": "ENGINE_STOP"})

    response = client.post("/commands/process_all")

    assert response.status_code == STATUS_CODE_OK

    data = response.json()

    assert len(data) == 2

    assert data[0]["status"] == "OK"
    assert data[0]["message"] == "ENGINE STARTED SUCCESFULLY"

    assert data[1]["status"] == "OK"
    assert data[1]["message"] == "ENGINE STOPPED SUCCESFULLY"

def test_missing_body():
    response = client.post("/commands/send", json={})
    assert response.status_code == STATUS_CODE_ERROR_NOBODY