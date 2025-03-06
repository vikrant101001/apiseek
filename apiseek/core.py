import os
import time
import datetime
import statistics
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
        method = request.method

        # Initialize overall metrics for the endpoint if not present.
        if path not in metrics:
            metrics[path] = {
                "requests": 0,
                "successful": 0,
                "failed": 0,
                "response_times": [],
                "by_method": {}
            }
        metrics[path]["requests"] += 1
        
        # Initialize metrics for the specific HTTP method.
        if method not in metrics[path]["by_method"]:
            metrics[path]["by_method"][method] = {
                "requests": 0,
                "successful": 0,
                "failed": 0,
                "response_times": [],
                "recent": None
            }
        metrics[path]["by_method"][method]["requests"] += 1

        # Start timer.
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as e:
            metrics[path]["failed"] += 1
            metrics[path]["by_method"][method]["failed"] += 1
            raise e
        # Calculate elapsed time.
        elapsed_time = time.perf_counter() - start_time
        
        # Record response time in overall and method-specific metrics.
        metrics[path]["response_times"].append(elapsed_time)
        metrics[path]["by_method"][method]["response_times"].append(elapsed_time)
        
        # Update the most recent call info.
        metrics[path]["by_method"][method]["recent"] = {
            "timestamp": datetime.datetime.now().isoformat(),
            "response_time": elapsed_time
        }
        
        # Update success/failure counts.
        if 200 <= response.status_code < 300:
            metrics[path]["successful"] += 1
            metrics[path]["by_method"][method]["successful"] += 1
        else:
            metrics[path]["failed"] += 1
            metrics[path]["by_method"][method]["failed"] += 1

        return response

def aggregate_times(times):
    """Compute average, minimum, maximum, and median response times."""
    if times:
        return {
            "avg": round(sum(times) / len(times), 3),
            "min": round(min(times), 3),
            "max": round(max(times), 3),
            "median": round(statistics.median(times), 3)
        }
    else:
        return {"avg": None, "min": None, "max": None, "median": None}

def init_app(app: FastAPI, prefix: str = "/apiseek"):
    """
    Initializes APISKEEK on a FastAPI app.
    
    - Registers a middleware to capture request metrics (including response times and method details).
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
        # Compute aggregated stats for each endpoint and each HTTP method.
        computed_stats = {}
        for endpoint, data in metrics.items():
            computed_stats[endpoint] = data.copy()
            computed_stats[endpoint]["response_stats"] = aggregate_times(data.get("response_times", []))
            computed_stats[endpoint]["by_method"] = {}
            for method, mdata in data.get("by_method", {}).items():
                computed_stats[endpoint]["by_method"][method] = mdata.copy()
                computed_stats[endpoint]["by_method"][method]["response_stats"] = aggregate_times(mdata.get("response_times", []))
        return templates.TemplateResponse("apiseek.html", {"request": request, "stats": computed_stats})
