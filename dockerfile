FROM python:latest

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY reqirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r reqirements.txt

# Copy the rest of the application code into the container
COPY ./Scripts /app/Scripts
COPY ./test.py /app/test.py
# Expose the port Jupyter runs on
EXPOSE 8888

CMD ["python", "test.py"]


