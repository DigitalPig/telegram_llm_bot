FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

# Copy the tutorial.py file into the container
COPY tutorial.py .

# Command to run the tutorial.py script
CMD ["python", "tutorial.py"]
