from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.middleware("http")
async def service_down_middleware(request: Request, call_next):
    # Bypass the middleware for the favicon route
    if request.url.path.startswith("/static") or request.url.path == "/favicon.ico":
        return await call_next(request)
    
    # Here you could add additional bypasses for other static resources if needed
    
    # Otherwise, respond with "service down"
    return templates.TemplateResponse("service_down.html", {"request": request}, status_code=503)

@app.get("/health")
async def health_check(request: Request):
    # An optional health check endpoint that returns the "Service is Down" page
    return templates.TemplateResponse("service_down.html", {"request": request}, status_code=503)
