import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Global dictionary to hold metrics for each endpoint.
metrics = {}

def _metrics_middleware(app: FastAPI):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        path = request.url.path
        if path not in metrics:
            metrics[path] = {"requests": 0, "successful": 0, "failed": 0}
        metrics[path]["requests"] += 1

        try:
            response = await call_next(request)
        except Exception as e:
            metrics[path]["failed"] += 1
            raise e

        # Consider any 2xx response as successful.
        if 200 <= response.status_code < 300:
            metrics[path]["successful"] += 1
        else:
            metrics[path]["failed"] += 1

        return response

def init_app(app: FastAPI, prefix: str = "/apiseek"):
    """
    Initializes APISKEEK on a FastAPI app.
    
    This function does the following:
    - Registers a middleware to capture request metrics.
    - Mounts static assets.
    - Registers a dashboard route at the given prefix (default: /apiseek).
    """
    # Register the metrics middleware.
    _metrics_middleware(app)

    # Determine paths for package assets.
    base_dir = os.path.dirname(__file__)
    static_path = os.path.join(base_dir, "static")
    templates_path = os.path.join(base_dir, "templates")

    # Mount static files under /apiseek/static.
    app.mount(prefix + "/static", StaticFiles(directory=static_path), name="apiseek_static")

    # Set up Jinja2 templates.
    templates = Jinja2Templates(directory=templates_path)

    # Define the dashboard endpoint.
    @app.get(prefix, response_class=HTMLResponse)
    async def apiseek_dashboard(request: Request):
        return templates.TemplateResponse("apiseek.html", {"request": request, "stats": metrics})
