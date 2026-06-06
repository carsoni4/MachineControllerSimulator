# Machine Controller Simulator

A Python-based machine controller simulator with automated tests and branch coverage.

This project simulates a simple embedded-style machine controller that accepts text commands, updates machine state, and returns structured command responses. It was built to practice Python automation, system-level testing, command validation, and test coverage concepts.

## Project Overview

The controller supports commands for:

* Starting and stopping the engine
* Setting engine speed
* Moving a bucket up or down
* Setting machine temperature
* Returning current machine status
* Handling invalid commands and unsafe operating conditions

The project includes a pytest-based automated test suite with line and branch coverage.

## Why I Built This

This project was created to practice skills used in embedded systems and automation testing roles, including:

* Writing automated tests in Python
* Testing controller-style command logic
* Validating expected system behavior
* Debugging failed test cases
* Measuring line and branch coverage
* Structuring a small Python project for maintainability

## Tech Stack

* Python
* pytest
* pytest-cov
* Git / GitHub

## Project Structure

```text
MachineControllerSimulator/
├── controller.py
├── test_controller.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Controller Features

The `MachineController` class tracks machine state such as:

```text
engine_running
engine_speed
temperature
bucket_position
warning
warning_message
```

Commands are sent using the `send_command()` method.

Example:

```python
controller = MachineController()

response = controller.send_command("ENGINE_START")

print(response.status)
print(response.message)
```

## Supported Commands

| Command                    | Description                            |
| -------------------------- | -------------------------------------- |
| `ENGINE_START`             | Starts the engine                      |
| `ENGINE_STOP`              | Stops the engine                       |
| `ENGINE_SPEED_SET <speed>` | Sets the engine speed                  |
| `BUCKET_MOVE_DOWN`         | Moves the bucket down if speed is safe |
| `BUCKET_MOVE_UP`           | Moves the bucket up if speed is safe   |
| `TEMP_SET <temperature>`   | Sets the machine temperature           |
| Invalid command            | Returns an error response              |

## Safety Rules

The controller includes simple safety validation rules:

* Engine speed cannot be set while the engine is off.
* Engine speed cannot be negative.
* The bucket cannot move if the machine speed is above the maximum safe bucket speed.
* A warning is triggered if temperature exceeds the maximum recommended temperature.
* Unknown commands return an error response.

## Running the Project

Clone the repository:

```bash
git clone <your-repo-url>
cd MachineControllerSimulator
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests With Coverage

Run line and branch coverage:

```bash
pytest -v --cov=machine_controller --cov-branch --cov-report=term-missing
```

Current Coverage result:

```text
============================================================ tests coverage 
____________________________________________ coverage: platform linux, python 3.12.3-final-0 
Name                               Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------
machine_controller/__init__.py         0      0      0      0   100%
machine_controller/constants.py        3      0      0      0   100%
machine_controller/controller.py      95      0     18      0   100%
machine_controller/enums.py           15      0      0      0   100%
machine_controller/logger.py           9      0      0      0   100%
machine_controller/models.py           6      0      0      0   100%
------------------------------------------------------------------------------
TOTAL                                128      0     18      0   100%
========================================================== 24 passed in 0.23s 
```

## What the Tests Cover

The automated tests cover:

* Engine start behavior
* Engine stop behavior
* Setting speed successfully
* Blocking speed changes when the engine is off
* Blocking negative speed values
* Moving the bucket up and down
* Blocking bucket movement at unsafe speeds
* Setting normal temperature values
* Triggering high-temperature warnings
* Returning machine status
* Handling unknown commands
* Handling command interactions with queue

## Example Test

```python
def test_queue_command():
    controller = MachineController()
    response = controller.queue_command(CommandAction.ENGINE_START.value)
    
    assert response.status == CommandStatus.OK
    assert response.message == f"COMMAND: {CommandAction.ENGINE_START.value} WAS ADDED TO QUEUE"
    assert controller.engine_running == False
```

## Key Concepts Practiced

This project demonstrates:

* Python classes and enums
* Command-based controller logic
* Automated testing with pytest
* Branch coverage with pytest-cov
* State validation
* Error handling
* Safety rule testing
* Clean test organization

## Future Improvements

Possible future additions:

* JSON-driven test cases
* Command logging
* UDP-based command interface
* More detailed machine status reporting
* Simulated intermittent failures for debugging practice
