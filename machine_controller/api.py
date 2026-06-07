from fastapi import FastAPI
from pydantic import BaseModel

from .controller import MachineController
from .models import CommandResponse

app = FastAPI(title="Machine Controller API")

controller = MachineController()

class CommandRequest(BaseModel):
    command: str

def response_to_dict(response: CommandResponse) -> dict:
    return {
        "status" : response.status,
        "message" : response.message
    }

@app.get("/status")
def get_status():
    return controller.get_machine_status()

@app.post("/commands/send")
def send_command(request: CommandRequest):
    response = controller.send_command(request.command)
    return response_to_dict(response)

@app.post("/commands/queue")
def queue_command(request: CommandRequest):
    response = controller.queue_command(request.command)
    return response_to_dict(response)

@app.post("/commands/process_next")
def process_next():
    response = controller.process_next_command()
    return response_to_dict(response)

@app.post("/commands/process_all")
def process_all():
    responses = controller.process_all_commands()
    for i in range(len(responses)):
        responses[i] = response_to_dict(responses[i])

    return responses
