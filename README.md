# GipaGram
This is a very simple Python3 Flask application that aims to create a very simple and minimal personal Instagram.<br/>
It also constitutes a testing ground to improve my skills with the Python language.

## gipagram-project setup!

### Linux OS - System requirements
Install and run Redis on Podman

    podman --version
    podman pull docker.io/redis:7
    mkdir -p ~/redis-data
    chmod 755 ~/redis-data

    podman run -d \
      --replace \
      --name redis \
      -p 6379:6379 \
      -v ~/redis-data:/data:Z \
      redis:7 \
      redis-server --appendonly yes

    podman logs redis

Install ffmpeg

    sudo dnf install file-libs ffmpeg
    
  or

    sudo apt install libmagic1 ffmpeg

### Linux OS - Python Environment
Prerequisites: Linux OS with Python v3.14.2 properly installed. <br/>
You can check the Python version installed running this command: <br/>

    python3 --version

Once you have done that, you can clone this repository in your local environment: <br/>

    git clone https://github.com/gpaolino/gipagram.git

In order to run this project, you need to create a virtual environment and populate it with the dependencies listed in requirements.txt <br/>
Run these commands to get started quickly: <br/>

    cd gipagram/
    python3 -m venv .venv
    source .venv/bin/activate

### Check if the correct virtual environment is active
Run the command:

    pip -V

Optionally upgrade pip package manager:

    python3 -m pip install --upgrade pip

Install all the dependencies:

    python3 -m pip install -r requirements.txt

### Run the application in Development mode
    cd src/
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
    # if you are using a Development VM on the same network:
    flask run --host=0.0.0.0 --port=5000
