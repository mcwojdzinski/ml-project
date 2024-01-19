# Use the official Python 3.11 image as the base image
FROM python:3.11

# Set the working directory to /app/ inside the container
WORKDIR /app/

# Copy only the requirements.txt file first to leverage Docker caching
COPY requirements.txt ./
COPY datasets/ datasets/
COPY test/ test/

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the contents of the local ml-project directory to /app/ in the image
COPY . /app/

# Set the command to run your application
CMD ["python3", "app/main.py"]
