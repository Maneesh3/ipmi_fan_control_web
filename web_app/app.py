from fastapi import FastAPI
import os
import subprocess

# Create a FastAPI instance
app = FastAPI()


def run_command():
    command = "ipmitool -V"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode == 0:  # Check if the command was successful
        print("Output:", result.stdout)
        return "Success", result.stdout
    else:
        print("Error:", result.stderr)
        return "Error", result.stdout


# Define a simple test endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/run")
def run_script(name: str):
    code, result = run_command()
    return {"Code":str(code),"response": str(result)}
