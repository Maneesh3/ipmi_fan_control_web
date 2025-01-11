from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess

# Create a FastAPI instance
app = FastAPI()


async def run_command():
    command = "ipmitool -V"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode == 0:  # Check if the command was successful
        print("Output:", result.stdout)
        return "Success", result.stdout
    else:
        print("Error:", result.stderr)
        return "Error", result.stdout


# Add CORS middleware (Optional, based on your use case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (useful for production readiness probes)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Define a simple test endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/run")
async def run_script():
    code, result = await run_command()
    return {"Code":str(code),"response": str(result)}

# Custom exception handler (example for improved error handling)
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"},
    )