import subprocess


def start_dev():
    subprocess.run(["uvicorn", "main:app", "--reload"])
