# FOOD_APP/Dockerfile

# 1. Base Image: Start from a specific, stable, and lightweight Python image.
#    This provides the Python runtime environment inside your container.
FROM python:3.8.10-slim-buster

# 2. Set Working Directory: All subsequent commands will be executed relative to /app inside the container.
#    This is where your application code will reside.
WORKDIR /app

# 3. Copy Requirements File First: This is a Docker build caching optimization.
#    If your 'requirements.txt' doesn't change, Docker can reuse the 'pip install' layer,
#    significantly speeding up subsequent builds.
COPY requirements.txt .

# Upgrade pip itself to ensure it has the latest index and features
RUN pip install --upgrade pip

# 4. Install Python Dependencies: Install all packages listed in requirements.txt.
#    '--no-cache-dir' reduces the final image size by not storing pip's download cache.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code: Copy the rest of your application's source code into /app.
#    This layer will change if your code changes, ensuring your latest code is always used.
COPY . .

# 6. Expose Port: Informs Docker that the container will listen on port 5000.
#    This is documentation, not an actual mapping. The mapping happens in docker-compose.yml.
EXPOSE 5000

# 7. Set Environment Variables: Configure your Flask application inside the container.
#    - FLASK_APP=app.py: Tells Flask where your main application instance is.
#    - FLASK_RUN_HOST=0.0.0.0: Tells Flask to listen on ALL network interfaces.
#      This is crucial for your app to be accessible from outside the container.
#    - FLASK_DEBUG=0: Sets Flask to production mode (disables debug, faster, more secure).
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=0

# 8. Define Command to Run: This is the command executed when a container starts from this image.
#    - For development and simple testing, 'flask run' is convenient.
#    - For production, you would typically switch to 'gunicorn' (which you've installed):
#      CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
CMD ["flask", "run"]