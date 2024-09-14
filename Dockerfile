FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN apt-get update && \ 
    apt-get -y install build-essential && \
    apt-get clean && \
    pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

# Copy the tutorial.py file into the container
COPY summary_bot.py .

# Command to run the tutorial.py script
CMD ["python", "summary_bot.py"]
