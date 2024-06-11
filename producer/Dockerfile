FROM python:3.9-slim

# Set working directory in the container and copy directory contents
WORKDIR /app
COPY . /app

# Install the dependencies
RUN pip install pika

# Run the producer script
CMD ["python", "producer.py"]