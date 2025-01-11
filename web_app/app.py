from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ipmi_cmd import run_command_test, fan_control_command

# Create a FastAPI instance
app = FastAPI()



# Mount the static directory to serve CSS and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configure Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

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
@app.get("/test")
async def test_page():
    return {"message": "Hello, FastAPI!"}

@app.get("/test_run")
async def run_script():
    code, result = await run_command_test()
    return {"Code":str(code),"response": str(result)}

@app.get("/")
async def root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": None})

# Process the submitted form data
@app.post("/")
async def submit_data(request: Request,
        username: str = Form(...), 
        password: str = Form(...), 
        ipaddress: str = Form(...), 
        fanspeed: int = Form(...)):
    request_data = {
        "username" : username, "password" : password, "ipaddress" : ipaddress, "fanspeed" : fanspeed
    }
    print(request_data)
    response_data = await fan_control_command(request_data)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "code": response_data["code"],
        "message": response_data["message"]
    })

# Custom exception handler (example for improved error handling)
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"},
    )