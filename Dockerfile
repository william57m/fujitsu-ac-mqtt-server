FROM arm32v7/python:3.9-buster

WORKDIR /code

# Copy the dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the sources
COPY src/ .

# Run
CMD [ "python", "./server.py" ]
