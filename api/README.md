# element61 backend API for internal chatbot

## Introduction 
This is the backend API developed in FLASK  with Python for the internal element61 chatbot.  

## Recommended Extensions

1. Ruff: A linting extension.

## Getting Started
1. Clone the repo
2. Switch to the dev branch
3. Create a python environment using VS CODE. Ctrl P, search for Create Environment, select Python 3.11 (Be sure to have installed upfront), select the requirements.txt
4. GO to the .venv\scripts folder and execute Activate.bat
5. Create a launch.json file in  your local .vscode folder with the following contents
```json 
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": false
        }
    ]
}
```
4. Press F5 to be able to debug locally, you can consume the endpoints with postman or any other tool
5. To consume for example the Private GPT just use the following url:
http://127.0.0.1:5000/privategptstream?prompt=tell%20me%20a%20joke%20about%20python%20developers
6. Place breakpoints as you wish.


## Contribute
1. Clone the repo
2. Create a branch from the DEV branch, example: features/newfeature.
3. After testing locally, merge your branch to DEV.
4. At this point CI and CD pipelines will be run on the DEV branch, make sure to test that your API modifications work on the DEV url:
https://webapp-chat-e61-03.azurewebsites.net/
5. Show your changes to the PM or Project Leaders (Floriant Sturm, Luis Valencia), Create a Pull Request and they will approve it.
6. CI and CD Pipelines will be run on the main branch, the production URL will be:
https://webapp-chat-e61-01.azurewebsites.net/
7. Delete the feature branch.

## Problems with CI/CD Pipeline
1. Run ```python deploy.py``` to deploy from your vs code folder directly to the Azure DEV enviroment. Only do this in a hurry, or when CI CD is not working properly.