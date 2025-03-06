# APISEEK

APISEEK is a one-stop shop for every FastAPI request, providing essential metrics and insights for each API endpoint. It’s ideal for individuals and organizations looking to easily monitor API usage, performance, and user interactions.

## Features

- **Real-time Metrics**: Track every FastAPI request as it happens.
- **Comprehensive Dashboard**: View data such as:
  - Request Name
  - Request Type (HTTP Method)
  - Total Requests (since server startup)
  - Successful Requests
  - Failed Requests
  - Average Response Time
  - Minimum Response Time
  - Median Response Time
  - Maximum Response Time
  - Most Recent Call (Timestamp & Response Time)

## Installation and Setup

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn

### Step 1: Prepare Your FastAPI Application

Ensure you have FastAPI and Uvicorn installed and your API endpoints are up and running. For example, you can install them via:

```bash
pip install fastapi uvicorn
```
### Step 3: Integrate APISKEEK into Your Application
Install apiseek

```bash
pip install apiseek==0.2
```

Add the following code to your FastAPI application (e.g., in your main.py):
```bash
from fastapi import FastAPI
from apiseek import init_app

app = FastAPI()

# Initialize APISKEEK (dashboard will be available at /apiseek)
init_app(app)

# Define your API endpoints below
@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}
```

### Dashboard
Run your application using Uvicorn:
```bash
uvicorn main:app --reload
```
Then, open your browser and navigate to
```bash
http://127.0.0.1:8000/apiseek
```
or
```bash
localhost:8000/apiseek
```
You'll see the clean, intuitive dashboard displaying all the key metrics for your API endpoints.

![apiseek1](https://github.com/user-attachments/assets/da022cd2-7276-4042-98da-05f44f490da1)

### Data Shown
Currently, the dashboard displays the following data for each API endpoint:

Request Name
Request Type
Total Requests (from server startup)
Successful Requests
Failed Requests
Average Response Time
Minimum Response Time
Median Response Time
Maximum Response Time
Most Recent Call
Response Time

### How to Contribute
Contributions are welcome! If you have suggestions, improvements, or bug fixes, please reach out:

Email: vikrant.th2014@gmail.com
LinkedIn: [Programming Vikrant](https://www.linkedin.com/in/programming-vikrant/)
Let's discuss new features and improvements that can take APISKEEK from version 0.2 to 0.5 and beyond. Once we reach a larger user base, we'll set up proper community channels and governance to further develop this project.

### License
APISKEEK is released under the MIT License.




