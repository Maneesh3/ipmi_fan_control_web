# Use the official Python Alpine base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install IPMI dependency
RUN apk add --no-cache ipmitool

# Install Python requirements
COPY web_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python file into the container
COPY web_app/ .

# Expose port 8080
EXPOSE 8080

# Specify the default command to run the Python script
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "app:app"]
