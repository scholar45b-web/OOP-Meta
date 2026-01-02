#READ_ME

This is a computer vison based flomodoro timer

Prerequisites: 
- Due to known errors of tensorflow due to incompatibilities to python version 3.13, the user is required to download Python 3.10 or 3.11
- A webcam is required for the full experience of the app

Installation steps
1. Unzip the file
2. Open VSCode
3. Open file
4. Create virtual environment
```python -m venv .venv```

{if the virtual environment fails to set up due to windows security,type the following into the terminal and enter}
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

5. Activate virtual environment
* *Windows:* `.venv\Scripts\activate`
* *Mac/Linux:* `source .venv/bin/activate`

6. Download the dependancies from requirements.txt
```pip install -r requirements.txt```

{if requirements.txt fails to manually run}
pip install deepface tf-keras opencv-python pillow numpy pandas
