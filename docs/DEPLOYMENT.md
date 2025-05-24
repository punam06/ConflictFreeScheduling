# Deployment Guide

This guide covers deploying the Conflict-Free Scheduling project for different environments and use cases.

## Table of Contents

- [Deployment Options](#deployment-options)
- [Local Development](#local-development)
- [Web Application Deployment](#web-application-deployment)
- [Academic/Educational Deployment](#academiceducational-deployment)
- [Production Considerations](#production-considerations)

## Deployment Options

### 1. Local Executable

**Best for**: Command-line usage, algorithm testing, educational demos

```bash
# Build the project
mkdir build && cd build
cmake ..
make

# Run the executable
./scheduler --help
./scheduler --algorithm greedy --input ../data/courses.txt
```

### 2. Academic Distribution

**Best for**: Educational use, student assignments

```bash
# Create distribution package
make install

# Copy to system path (optional)
sudo cp ./scheduler /usr/local/bin/

# Create academic package
tar -czf ConflictFreeScheduling-v1.0.tar.gz \
    src/ docs/ examples/ tests/ CMakeLists.txt Makefile README.md
```
    "\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from src.algorithms.greedy import greedy_activity_selection\n",
    "from src.utils.data_generator import generate_random_activities\n",
    "from src.utils.visualization import plot_schedule\n",
    "\n",
    "# Generate sample CSE course data\n",
    "courses = [\n",
    "    ('Data Structures', 9, 11),\n",
    "    ('Algorithms', 10, 12),\n",
    "    ('Database Systems', 13, 15),\n",
    "    ('Computer Networks', 14, 16),\n",
    "    ('Software Engineering', 16, 18)\n",
    "]\n",
    "\n",
    "activities = [(start, end) for _, start, end in courses]\n",
    "print(\"CSE Course Schedule:\")\n",
    "for i, (name, start, end) in enumerate(courses):\n",
    "    print(f\"{i}: {name} ({start}:00 - {end}:00)\")\n",
    "\n",
    "# Apply greedy algorithm\n",
    "selected = greedy_activity_selection(activities)\n",
    "print(f\"\\nSelected courses: {[courses[i][0] for i in selected]}\")\n",
    "\n",
    "# Visualize results\n",
    "plot_schedule(activities, selected, \"CSE Course Scheduling\")\n",
    "plt.show()"
   ]
  }
 ]
}
```

### 2. Streamlit Web App

**Best for**: Interactive web demonstrations

```bash
# Install Streamlit
pip install streamlit

# Create web app
streamlit run web/app.py
```

Create `web/app.py`:

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.algorithms.greedy import greedy_activity_selection
from src.algorithms.dynamic_programming import dp_activity_selection
from src.utils.visualization import plot_schedule

st.title("🎯 Conflict-Free Scheduling Demo")
st.markdown("### CSE Department Course Scheduling System")

# Sidebar for algorithm selection
algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Greedy", "Dynamic Programming", "Branch & Bound"]
)

# Sample data
st.header("📊 Input Data")
courses_data = [
    ("Data Structures", 9, 11, 50),
    ("Algorithms", 10, 12, 45),
    ("Database Systems", 13, 15, 40),
    ("Computer Networks", 14, 16, 35),
    ("Software Engineering", 16, 18, 30),
    ("Machine Learning", 15, 17, 60)
]

df = pd.DataFrame(courses_data, 
                 columns=["Course", "Start", "End", "Students"])
st.dataframe(df)

# Run algorithm
if st.button("🚀 Schedule Courses"):
    activities = [(row.Start, row.End) for _, row in df.iterrows()]
    
    if algorithm == "Greedy":
        selected = greedy_activity_selection(activities)
    elif algorithm == "Dynamic Programming":
        weights = df["Students"].tolist()
        selected, total_weight = dp_activity_selection(activities, weights)
        st.success(f"Total Students Accommodated: {total_weight}")
    
    # Display results
    st.header("📅 Scheduled Courses")
    selected_courses = df.iloc[selected]
    st.dataframe(selected_courses)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    plot_schedule(activities, selected, f"Schedule using {algorithm} Algorithm")
    st.pyplot(fig)
```

### 3. Flask REST API

**Best for**: Integration with other systems

```bash
# Install Flask
pip install flask flask-cors

# Run API server
python api/app.py
```

Create `api/app.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.algorithms.greedy import greedy_activity_selection
from src.algorithms.dynamic_programming import dp_activity_selection

app = Flask(__name__)
CORS(app)

@app.route('/api/schedule', methods=['POST'])
def schedule_activities():
    try:
        data = request.json
        activities = data.get('activities', [])
        weights = data.get('weights', None)
        algorithm = data.get('algorithm', 'greedy')
        
        if algorithm == 'greedy':
            selected = greedy_activity_selection(activities)
            result = {
                'selected_indices': selected,
                'algorithm': 'greedy',
                'total_activities': len(selected)
            }
        elif algorithm == 'dp':
            if weights:
                selected, total_weight = dp_activity_selection(activities, weights)
                result = {
                    'selected_indices': selected,
                    'total_weight': total_weight,
                    'algorithm': 'dynamic_programming'
                }
            else:
                selected = dp_activity_selection(activities)
                result = {
                    'selected_indices': selected,
                    'algorithm': 'dynamic_programming'
                }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Academic/Educational Deployment

### 1. GitHub Pages Documentation

Deploy documentation as a static website:

```yaml
# .github/workflows/docs.yml
name: Deploy Documentation

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install mkdocs mkdocs-material
    
    - name: Build docs
      run: mkdocs build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
```

### 2. Binder for Interactive Notebooks

Create `binder/environment.yml`:

```yaml
name: conflict-free-scheduling
channels:
  - conda-forge
dependencies:
  - python=3.9
  - numpy
  - matplotlib
  - pandas
  - jupyter
  - pip
  - pip:
    - pytest
    - memory-profiler
```

Add Binder badge to README:

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yourusername/ConflictFreeScheduling/main)
```

### 3. Colab Integration

Create Google Colab notebooks:

```python
# In Colab notebook
!git clone https://github.com/yourusername/ConflictFreeScheduling.git
%cd ConflictFreeScheduling
!pip install -r requirements.txt

# Run examples
from src.algorithms.greedy import greedy_activity_selection
# ... rest of code
```

## Docker Deployment

### Development Container

```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Copy source code
COPY . .

# Development server
CMD ["python", "-m", "pytest", "tests/", "-v"]
```

### Production Container

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install production dependencies only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY api/ ./api/

# Run API server
EXPOSE 5000
CMD ["python", "api/app.py"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEBUG=False
    volumes:
      - ./data:/app/data

  frontend:
    build: ./web
    ports:
      - "8501:8501"
    depends_on:
      - api

  jupyter:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8888:8888"
    command: jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
    volumes:
      - ./notebooks:/app/notebooks
```

## Cloud Deployment

### Heroku Deployment

Create `Procfile`:

```
web: python api/app.py
```

Create `runtime.txt`:

```
python-3.9.16
```

Deploy commands:

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create conflict-free-scheduling

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS Deployment

Using AWS Lambda:

```python
# lambda_function.py
import json
from src.algorithms.greedy import greedy_activity_selection

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        activities = body['activities']
        algorithm = body.get('algorithm', 'greedy')
        
        if algorithm == 'greedy':
            result = greedy_activity_selection(activities)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'selected_indices': result,
                'algorithm': algorithm
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
```

## Performance Considerations

### 1. Optimization for Large Datasets

```python
# Use numpy for better performance
import numpy as np

def optimized_greedy(activities):
    """Optimized version using numpy"""
    activities_np = np.array(activities)
    sorted_indices = np.argsort(activities_np[:, 1])  # Sort by finish time
    
    selected = [sorted_indices[0]]
    last_finish = activities_np[sorted_indices[0], 1]
    
    for idx in sorted_indices[1:]:
        if activities_np[idx, 0] >= last_finish:
            selected.append(idx)
            last_finish = activities_np[idx, 1]
    
    return selected
```

### 2. Caching for Web Applications

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_schedule(activities_tuple, algorithm='greedy'):
    """Cached version for repeated calls"""
    activities = list(activities_tuple)
    
    if algorithm == 'greedy':
        return greedy_activity_selection(activities)
    # ... other algorithms
```

### 3. Async Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def schedule_async(activities, algorithm='greedy'):
    """Async version for web applications"""
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor() as executor:
        if algorithm == 'greedy':
            result = await loop.run_in_executor(
                executor, greedy_activity_selection, activities
            )
        return result
```

## Monitoring and Logging

### Application Logging

```python
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def logged_schedule(activities, algorithm='greedy'):
    """Version with logging"""
    start_time = time.time()
    logger.info(f"Starting {algorithm} algorithm with {len(activities)} activities")
    
    try:
        if algorithm == 'greedy':
            result = greedy_activity_selection(activities)
        
        execution_time = time.time() - start_time
        logger.info(f"Algorithm completed in {execution_time:.4f}s, selected {len(result)} activities")
        
        return result
        
    except Exception as e:
        logger.error(f"Algorithm failed: {str(e)}")
        raise
```

### Performance Monitoring

```python
import psutil
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = []
    
    def monitor_execution(self, func, *args, **kwargs):
        # Before execution
        start_time = time.time()
        start_memory = psutil.virtual_memory().used
        start_cpu = psutil.cpu_percent()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # After execution
        end_time = time.time()
        end_memory = psutil.virtual_memory().used
        end_cpu = psutil.cpu_percent()
        
        metrics = {
            'execution_time': end_time - start_time,
            'memory_used': end_memory - start_memory,
            'cpu_usage': end_cpu - start_cpu,
            'timestamp': time.time()
        }
        
        self.metrics.append(metrics)
        return result, metrics

# Usage
monitor = PerformanceMonitor()
result, metrics = monitor.monitor_execution(
    greedy_activity_selection, activities
)
```

## Security Considerations

### Input Validation

```python
def validate_activities(activities):
    """Validate input activities"""
    if not isinstance(activities, list):
        raise ValueError("Activities must be a list")
    
    for i, activity in enumerate(activities):
        if not isinstance(activity, (list, tuple)) or len(activity) != 2:
            raise ValueError(f"Activity {i} must have start and end time")
        
        start, end = activity
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise ValueError(f"Activity {i} times must be numeric")
        
        if start >= end:
            raise ValueError(f"Activity {i} start time must be before end time")
    
    return True
```

### Rate Limiting (for APIs)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/schedule', methods=['POST'])
@limiter.limit("10 per minute")
def schedule_activities():
    # ... implementation
```

---

*This deployment guide covers various scenarios from academic presentations to production web applications. Choose the deployment option that best fits your use case.*
